"""psy-ugrid decoder for UGRID conventions

This module defines the decoder that we use to decode the UGRID conventions.
It is supposed to overwrite the one defined in the :mod:`psyplot.data` module
and has been originally developed in

https://codebase.helmholtz.cloud/psyplot/psyplot/-/merge_requests/31
"""

# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: LGPL-3.0-only


from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List
from warnings import warn

import numpy as np
import psyplot.data as psyd
import xarray as xr
from psyplot.docstring import docstrings

if TYPE_CHECKING:
    from psy_ugrid.ugrid import UGrid


xr_version = tuple(map(int, xr.__version__.split(".")[:2]))


class UGridDecoder(psyd.CFDecoder):
    """Decoder for UGrid data sets."""

    #: mapping from grid name to the :class:`gridded.pyugrid.ugrid.UGrid`
    # object representing it
    _grids: Dict[str, UGrid] = {}

    #: True if the data of the CFDecoder supports the extraction of a subset of
    #: the data based on the indices.
    #:
    #: For UGRID conventions, this is not easily possible because the
    #: extraction of a subset breaks the connectivity information of the mesh
    supports_spatial_slicing: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grids = {}

    def clear_cache(self):
        """Clear the cache and remove the UGRID instances."""
        self._grids.clear()

    def is_unstructured(self, *args, **kwargs):
        """Reimpletemented to return always True. Any ``*args`` and ``**kwargs``
        are ignored"""
        return True

    @docstrings.get_sections(base="UGridDecoder.get_mesh")
    def get_mesh(self, var, coords=None):
        """Get the mesh variable for the given `var`

        Parameters
        ----------
        var: xarray.Variable
            The data source whith the ``'mesh'`` attribute
        coords: dict
            The coordinates to use. If None, the coordinates of the dataset of
            this decoder is used

        Returns
        -------
        xarray.Coordinate
            The mesh coordinate"""
        mesh = var.attrs.get("mesh")
        if mesh is None:
            return None
        if coords is None:
            coords = self.ds.coords
        return coords.get(mesh, self.ds.coords.get(mesh))

    @docstrings.with_indent(8)
    def get_ugrid(self, var, coords=None, loc="infer"):
        """Get the :class:`~gridded.pyugrid.ugrid.UGrid` mesh object.

        This method creates a :class:`gridded.pyugrid.ugrid.UGrid` object for
        a given variable, depending on the corresponding ``'mesh'`` attribute.

        Parameters
        ----------
        %(UGridDecoder.get_mesh.parameters)s
        dual: {"infer", "node", "edge", "face"}
            If "node" or "edge", the dual grid will be computed.

        Returns
        -------
        gridded.pyugrid.ugrid.UGrid
            The UGrid object representing the mesh.
        """
        from psy_ugrid.ugrid import UGrid

        def get_coord(cname, raise_error=True):
            try:
                ret = coords[cname]
            except KeyError:
                if cname not in self.ds.coords:
                    if raise_error:
                        raise
                    return None
                else:
                    ret = self.ds.coords[cname]
                    try:
                        idims = var.psy.idims
                    except AttributeError:  # got xarray.Variable
                        idims = {}
                    ret = ret.isel(
                        **{d: sl for d, sl in idims.items() if d in ret.dims}
                    )
            if "start_index" in ret.attrs:
                return ret - int(ret.start_index)
            else:
                return ret

        mesh = self.get_mesh(var, coords)

        if not mesh:
            mesh = self.get_mesh(var)

        if not mesh:
            raise ValueError(
                "Could not find the mesh variable in the coordinates."
            )

        if mesh.name in self._grids:
            grid = self._grids[mesh.name]
        else:
            required_parameters = ["faces"]

            parameters = {
                "faces": "face_node_connectivity",
                "face_face_connectivity": "face_face_connectivity",
                "edges": "edge_node_connectivity",
                "boundaries": "boundary_node_connectivity",
            }

            coord_parameters = {
                "face_coordinates": "face_coordinates",
                "edge_coordinates": "edge_coordinates",
                "boundary_coordinates": "boundary_coordinates",
            }

            x_nodes, y_nodes = self.get_nodes(mesh, coords)

            kws = {
                "node_lon": x_nodes,
                "node_lat": y_nodes,
                "mesh_name": mesh.name,
            }

            coords = dict(coords or {})

            # check for face_dimension and edge_dimension and make sure they
            # appear last in the list
            if "face_dimension" in mesh.attrs:
                cname = mesh.attrs["face_node_connectivity"]
                faces = get_coord(cname)
                coords[cname] = faces.transpose(
                    mesh.attrs["face_dimension"], ...
                )

            if (
                "edge_dimension" in mesh.attrs
                and "edge_node_connectivity" in mesh.attrs
            ):
                cname = mesh.attrs["edge_node_connectivity"]
                edges = get_coord(cname)
                coords[cname] = edges.transpose(
                    mesh.attrs["edge_dimension"], ...
                )

            if (
                "edge_dimension" in mesh.attrs
                and "edge_face_connectivity" in mesh.attrs
            ):
                cname = mesh.attrs["edge_face_connectivity"]
                ef_conn = get_coord(cname)
                coords[cname] = ef_conn.transpose(
                    mesh.attrs["edge_dimension"], ...
                )

            for key, attr in parameters.items():
                if attr in mesh.attrs:
                    coord = get_coord(
                        mesh.attrs[attr], key in required_parameters
                    )
                    if coord is not None:
                        kws[key] = coord.values

            for key, attr in coord_parameters.items():
                if attr in mesh.attrs:
                    xname, yname = mesh.attrs[attr].split()
                    kws[key] = np.dstack([get_coord(xname), get_coord(yname)])[
                        0
                    ]

            # now we have to turn NaN into masked integer arrays
            for param in parameters:
                if kws.get(param) is not None:
                    arr = kws[param]
                    mask = np.isnan(arr)
                    if mask.any():
                        arr = np.where(mask, -999, arr).astype(int)
                    kws[param] = np.ma.masked_where(mask, arr)

            grid = UGrid(**kws)
            self._grids[mesh.name] = grid

        # create the dual mesh if necessary
        if loc == "infer":
            loc = self.infer_location(var, coords, grid)

        if loc in ["node", "edge"]:
            dual_name = grid.mesh_name + "_dual_" + loc
            if dual_name in self._grids:
                grid = self._grids[dual_name]
            else:
                grid = grid.create_dual_mesh(loc)
                grid.mesh_name = dual_name
                self._grids[dual_name] = grid

        return grid

    @classmethod
    @docstrings.dedent
    def can_decode(cls, ds, var):
        """
        Check whether the given variable can be decoded.

        Returns True if a mesh coordinate could be found via the
        :meth:`get_mesh` method

        Parameters
        ----------
        %(CFDecoder.can_decode.parameters)s

        Returns
        -------
        %(CFDecoder.can_decode.returns)s"""
        return cls(ds).get_mesh(var) is not None

    @docstrings.dedent
    def get_triangles(
        self,
        var,
        coords=None,
        convert_radian=True,
        copy=False,
        src_crs=None,
        target_crs=None,
        nans=None,
        stacklevel=1,
    ):
        """
        Get the of the given coordinate.

        Parameters
        ----------
        %(CFDecoder.get_triangles.parameters)s

        Returns
        -------
        %(CFDecoder.get_triangles.returns)s

        Notes
        -----
        If the ``'location'`` attribute is set to ``'node'``, a delaunay
        triangulation is performed using the
        :class:`matplotlib.tri.Triangulation` class.

        .. todo::
            Implement the visualization for UGrid data shown on the edge of the
            triangles"""
        warn(
            "The 'get_triangles' method is depreceated and will be removed "
            "soon! Use the 'get_cell_node_coord' method!",
            DeprecationWarning,
            stacklevel=stacklevel,
        )
        from matplotlib.tri import Triangulation

        if coords is None:
            coords = self.ds.coords

        def get_coord(coord):
            return coords.get(coord, self.ds.coords.get(coord))

        mesh = self.get_mesh(var, coords)
        nodes = self.get_nodes(mesh, coords)
        if any(n is None for n in nodes):
            raise ValueError("Could not find the nodes variables!")
        xvert, yvert = nodes
        xvert = xvert.values
        yvert = yvert.values
        loc = var.attrs.get("location", "face")
        if loc == "face":
            triangles = get_coord(
                mesh.attrs.get("face_node_connectivity", "")
            ).values
            if triangles is None:
                raise ValueError(
                    "Could not find the connectivity information!"
                )
        elif loc == "node":
            triangles = None
        else:
            raise ValueError(
                "Could not interprete location attribute (%s) of mesh "
                "variable %s!" % (loc, mesh.name)
            )

        if convert_radian:
            for coord in nodes:
                if coord.attrs.get("units") == "radian":
                    coord = coord * 180.0 / np.pi
        if src_crs is not None and src_crs != target_crs:
            if target_crs is None:
                raise ValueError(
                    "Found %s for the source crs but got None for the "
                    "target_crs!" % (src_crs,)
                )
            xvert = xvert[triangles].ravel()
            yvert = yvert[triangles].ravel()
            arr = target_crs.transform_points(src_crs, xvert, yvert)
            xvert = arr[:, 0]
            yvert = arr[:, 1]
            if loc == "face":
                triangles = np.reshape(range(len(xvert)), (len(xvert) // 3, 3))

        return Triangulation(xvert, yvert, triangles)

    @docstrings.dedent
    def get_cell_node_coord(self, var, coords=None, axis="x", nans=None):
        """
        Checks whether the bounds in the variable attribute are triangular

        Parameters
        ----------
        %(CFDecoder.get_cell_node_coord.parameters)s

        Returns
        -------
        %(CFDecoder.get_cell_node_coord.returns)s"""
        if coords is None:
            coords = self.ds.coords

        idims = self.get_coord_idims(coords)

        def get_coord(coord):
            coord = coords.get(coord, self.ds.coords.get(coord))
            return coord.isel(
                **{d: sl for d, sl in idims.items() if d in coord.dims}
            )

        mesh = self.get_mesh(var, coords)
        if mesh is None:
            return
        nodes = self.get_nodes(mesh, coords)
        if not len(nodes):
            raise ValueError(
                "Could not find the nodes variables for the %s "
                "coordinate!" % axis
            )
        vert = nodes[0 if axis == "x" else 1]
        if vert is None:
            raise ValueError(
                "Could not find the nodes variables for the %s "
                "coordinate!" % axis
            )

        grid = self.get_ugrid(var, coords)

        faces = grid.faces
        if np.ma.isMA(faces) and faces.mask.any():
            isnull = faces.mask
            faces = faces.filled(-999).astype(int)
            for i in range(faces.shape[1]):
                mask = isnull[:, i]
                if mask.any():
                    for j in range(i, faces.shape[1]):
                        faces[mask, j] = faces[mask, j - i]

        node = grid.nodes[..., 0 if axis == "x" else 1]
        bounds = node[faces]

        loc = self.infer_location(var, coords)

        dim0 = "__face" if loc == "node" else var.dims[-1]
        return xr.DataArray(
            bounds,
            coords={
                key: val for key, val in coords.items() if (dim0,) == val.dims
            },
            dims=(
                dim0,
                "__bnds",
            ),
            name=vert.name + "_bnds",
            attrs=vert.attrs.copy(),
        )

    @docstrings.with_indent(8)
    def infer_location(self, var, coords=None, grid=None):
        """Infer the location for the variable.

        Parameters
        ----------
        %(UGridDecoder.get_mesh.parameters)s
        grid: gridded.pyugrid.ugrid.UGrid
            The grid for this variable. If None, it will be created using the
            :meth:`get_ugrid` method (if necessary)

        Returns
        -------
        str
            ``"node"``, ``"face"`` or ``"edge"``
        """
        if coords is None:
            coords = self.ds.coords
        if not var.attrs.get("location"):
            if grid is None:
                grid = self.get_ugrid(var, coords, loc="face")
            # get the axis of the spatial dimension by looking up possible
            # dimension names. We cannot use get_xname here because this uses
            # infer_location
            mesh = self.get_mesh(var, coords)
            possible_dims = set()
            for attr in [
                "node_coordinates",
                "edge_coordinates",
                "face_coordinates",
            ]:
                if attr in mesh.attrs:
                    for vname in mesh.attrs[attr].split():
                        cvar = coords.get(vname)
                        if cvar is not None:
                            possible_dims.update(cvar.dims)
            for attr in [
                "face_node_connectivity",
                "edge_node_connectivity",
                "face_edge_connectivity",
                "face_face_connectivity",
                "edge_face_connectivity",
            ]:
                vname = mesh.attrs.get(attr)
                if vname:
                    cvar = coords.get(vname)
                    if cvar is not None:
                        possible_dims.update(cvar.dims)
            found = possible_dims.intersection(var.dims)
            if found and len(found) == 1:
                axis = var.dims.index(next(iter(found)))
            else:
                axis = -1
            loc = grid.infer_location(var, axis)
        else:
            loc = var.attrs["location"]
        return loc

    @staticmethod
    @docstrings.dedent
    def decode_coords(ds, gridfile=None):
        """
        Reimplemented to set the mesh variables as coordinates

        Parameters
        ----------
        %(CFDecoder.decode_coords.parameters)s

        Returns
        -------
        %(CFDecoder.decode_coords.returns)s"""
        extra_coords = set(ds.coords)
        if gridfile is not None and not isinstance(gridfile, xr.Dataset):
            gridfile = psyd.open_dataset(gridfile)
        for var in ds.variables.values():
            if "mesh" in var.attrs:
                mesh = var.attrs["mesh"]
                if mesh not in extra_coords:
                    extra_coords.add(mesh)
                    try:
                        mesh_var = ds.variables[mesh]
                    except KeyError:
                        if gridfile is not None:
                            try:
                                mesh_var = gridfile.variables[mesh]
                            except KeyError:
                                warn("Could not find mesh variable %s" % mesh)
                                continue
                        else:
                            warn("Could not find mesh variable %s" % mesh)
                            continue

                    parameters = [
                        "node_coordinates",
                        "face_node_connectivity",
                        "face_face_connectivity",
                        "edge_node_connectivity",
                        "edge_face_connectivity",
                        "boundary_node_connectivity",
                        "face_coordinates",
                        "edge_coordinates",
                        "boundary_coordinates",
                    ]

                    for param in parameters:
                        if param in mesh_var.attrs:
                            extra_coords.update(mesh_var.attrs[param].split())
        if gridfile is not None:
            ds.update(
                {
                    k: v
                    for k, v in gridfile.variables.items()
                    if k in extra_coords
                }
            )
        if xr_version < (0, 11):
            ds.set_coords(
                extra_coords.intersection(ds.variables), inplace=True
            )
        else:
            ds._coord_names.update(extra_coords.intersection(ds.variables))
        return ds

    def get_nodes(self, coord, coords=None):
        """Get the variables containing the definition of the nodes

        Parameters
        ----------
        coord: xarray.Coordinate
            The mesh variable
        coords: dict, optional
            The coordinates to use to get node coordinates"""
        if coords is None:
            coords = {}

        def get_coord(coord):
            return coords.get(coord, self.ds.coords.get(coord))

        return list(
            map(get_coord, coord.attrs.get("node_coordinates", "").split()[:2])
        )

    @docstrings.with_indent(8)
    def get_xname(self, var, coords=None):
        """Get the name of the spatial dimension

        Parameters
        ----------
        %(CFDecoder.get_y.parameters)s

        Returns
        -------
        str
            The dimension name
        """

        def get_dim(name):
            coord = coords.get(
                name, ds.coords.get(name, ds.variables.get(name))
            )
            if coord is None:
                raise KeyError(f"Missing {loc} coordinate {name}")
            else:
                return coord.dims[0]

        ds = self.ds
        loc = self.infer_location(var, coords)
        mesh = self.get_mesh(var, coords)
        coords = coords or ds.coords
        if loc == "node":
            return get_dim(mesh.node_coordinates.split()[0])
        elif loc == "edge":
            return get_dim(mesh.edge_node_connectivity)
        else:
            return get_dim(mesh.face_node_connectivity)

    @docstrings.with_indent(8)
    def get_yname(self, var, coords=None):
        """Get the name of the spatial dimension

        Parameters
        ----------
        %(CFDecoder.get_y.parameters)s

        Returns
        -------
        str
            The dimension name
        """
        return self.get_xname(var, coords)  # x- and y-dimensions are the same

    @docstrings.with_indent(8)
    def get_zname(self, var, coords=None):
        """Get the name of the vertical dimension

        Parameters
        ----------
        %(CFDecoder.get_y.parameters)s

        Returns
        -------
        str
            The dimension name
        """
        # reimplement to make sure we do not interfere with x- and y-dimension

        dim = super().get_zname(var, coords)

        t_or_x = [self.get_tname(var, coords), self.get_xname(var, coords)]

        if dim and var.dims and dim in t_or_x:
            # wrong dimension has been chosen by the default approach
            for dim in var.dims:
                if dim not in t_or_x:
                    break
        return dim

    @docstrings.dedent
    def get_x(self, var, coords=None):
        """
        Get the centers of the triangles in the x-dimension

        Parameters
        ----------
        %(CFDecoder.get_y.parameters)s

        Returns
        -------
        %(CFDecoder.get_y.returns)s"""
        if coords is None:
            coords = self.ds.coords
        # first we try the super class
        ret = super(UGridDecoder, self).get_x(var, coords)
        # but if that doesn't work because we get the variable name in the
        # dimension of `var`, we use the means of the faces
        if (
            ret is None
            or ret.name in var.dims
            or (hasattr(var, "mesh") and ret.name == var.mesh)
        ):
            loc = self.infer_location(var, coords)
            x = self.get_nodes(self.get_mesh(var, coords), coords)[0]
            if loc == "node":
                return x
            else:
                grid = self.get_ugrid(var, coords, loc)
                if grid.face_coordinates is None:
                    grid.build_face_coordinates()
                try:
                    cls = xr.IndexVariable
                except AttributeError:  # xarray < 0.9
                    cls = xr.Coordinate
                return cls(
                    x.name, grid.face_coordinates[..., 0], attrs=x.attrs.copy()
                )
        else:
            return ret

    @docstrings.dedent
    def get_y(self, var, coords=None):
        """
        Get the centers of the triangles in the y-dimension

        Parameters
        ----------
        %(CFDecoder.get_y.parameters)s

        Returns
        -------
        %(CFDecoder.get_y.returns)s"""
        if coords is None:
            coords = self.ds.coords
        # first we try the super class
        ret = super(UGridDecoder, self).get_y(var, coords)
        # but if that doesn't work because we get the variable name in the
        # dimension of `var`, we use the means of the triangles
        if (
            ret is None
            or ret.name in var.dims
            or (hasattr(var, "mesh") and ret.name == var.mesh)
        ):
            loc = self.infer_location(var, coords)
            y = self.get_nodes(self.get_mesh(var, coords), coords)[1]
            if loc == "node":
                return y
            else:
                grid = self.get_ugrid(var, coords, loc)
                if grid.face_coordinates is None:
                    grid.build_face_coordinates()
                try:
                    cls = xr.IndexVariable
                except AttributeError:  # xarray < 0.9
                    cls = xr.Coordinate
                return cls(
                    y.name, grid.face_coordinates[..., 1], attrs=y.attrs.copy()
                )
        else:
            return ret

    def get_metadata_sections(self, var: xr.DataArray) -> List[str]:
        # reimplemented to add the Mesh information
        return super().get_metadata_sections(var) + ["Mesh information"]

    get_metadata_sections.__doc__ = (
        psyd.CFDecoder.get_metadata_sections.__doc__
    )

    def get_metadata_for_section(
        self, var: xr.DataArray, section: str, coords: Dict
    ) -> Dict[str, str]:
        # reimplemented to account for the mesh variable
        if section == "Mesh information":
            try:
                mesh = coords[var.attrs["mesh"]]
            except KeyError:
                raise ValueError(
                    f"Could not find mesh variable {var.attrs['mesh']}"
                    f"in the coordinates {tuple(coords)}"
                )
            else:
                return {key: str(val) for key, val in mesh.attrs.items()}
        else:
            return super().get_metadata_for_section(var, section, coords)
