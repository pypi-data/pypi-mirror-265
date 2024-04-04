#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: LGPL-3.0-only

"""
ugrid classes

set of classes for working with unstructured model grids

The "ugrid" class is the base class: it stores everything in memory

It can read from and write to netcdf files in the UGRID format.

It may be able to reference a netcdf file at some point, rather than storing
directly in memory.

NOTE: only tested for triangular and quad mesh grids at the moment.

NOTE: This code has been extracted from the pull request by @Chilipp to the
gridded package, at https://github.com/NOAA-ORR-ERD/gridded/pull/62/.
Gridded is licensed under the Unlicense.

"""

from __future__ import absolute_import, division, print_function

import numpy as np

# datatype used for indexes -- might want to change for 64 bit some day.
IND_DT = np.int32
NODE_DT = np.float64  # datatype used for node coordinates.


class UGrid(object):
    """
    A basic class to hold an unstructured grid as defined in the UGrid convention.

    The internal structure mirrors the netcdf data standard.
    """

    def __init__(
        self,
        nodes=None,
        node_lon=None,
        node_lat=None,
        faces=None,
        edges=None,
        boundaries=None,
        face_face_connectivity=None,
        face_edge_connectivity=None,
        edge_coordinates=None,
        face_coordinates=None,
        boundary_coordinates=None,
        data=None,
        mesh_name="mesh",
        edge_face_connectivity=None,
        edge_orientation=None,
    ):
        """
        ugrid class -- holds, saves, etc. an unstructured grid

        :param nodes=None : the coordinates of the nodes
        :type nodes: (NX2) array of floats

        :param faces=None : the faces of the grid. Indexes for the nodes array.
        :type faces: (NX3) array of integers

        :param edges=None : the edges of the grid. Indexes for the nodes array.
        :type edges: (NX2) array of integers

        :param boundaries=None: specification of the boundaries are usually a
                                subset of edges where boundary condition
                                information, etc is stored.
                                (NX2) integer array of indexes for the nodes
                                array.
        :type boundaries: numpy array of integers

        :param face_face_connectivity=None: connectivity arrays.
        :param face_edge_connectivity=None: connectivity arrays.

        :param edge_coordinates=None: representative coordinate of the edges.
        :param face_coordinates=None: representative coordinate of the faces.
        :param boundary_coordinates=None: representative coordinate of the
                                          boundaries.

        :param edge_coordinates=None: representative coordinate of the edges
        :type edge_coordinates: (NX2) array of floats

        :param face_coordinates=None: representative coordinate of the faces
                                      (NX2) float array
        :type face_coordinates: (NX2) array of floats


        :param boundary_coordinates=None: representative coordinate of the
                                          boundaries
        :type boundary_coordinates: (NX2) array of floats


        :param data = None: associated variables
        :type data: dict of UVar objects

        :param mesh_name = "mesh": optional name for the mesh
        :type mesh_name: string

        :param edge_face_connectivity=None: optional mapping from edge to
                                            attached face index
        :type edge_face_connectivity: (Nx2) array of ints

        :param edge_orientation=None: the orientation for each edge within the
                                      corresponding face from the
                                      `edge_face_connectivity`. ``1`` means,
                                      the edge has the same orientation in
                                      :attr:`faces` and :attr:`edges`, ``-1``
                                      means the opposite.
        :type edge_orientation: (Nx2) masked array of ints with the same shape
                                      as the `edge_face_connectivity` (i.e.
                                      shape ``(n_edges, 2)``)

        Often this is too much data to pass in as literals -- so usually
        specialized constructors will be used instead (load from file, etc).

        The index variables faces can be a masked array. The mask is
        used for so called flexible meshes. Flexible meshes contain
        cells with varying number of nodes per face.  See the flexible
        mesh section in the convention for further details.
        """

        if (nodes is not None) and (
            (node_lon is not None) or (node_lat is not None)
        ):
            raise TypeError(
                "You need to provide a single nodes array "
                "or node_lon and node_lat"
            )
        if nodes is None:
            if node_lon is not None and node_lat is not None:
                nodes = np.ma.column_stack((node_lon, node_lat))
        self.nodes = nodes
        self.faces = faces
        self.edges = edges
        self.boundaries = boundaries

        self.face_face_connectivity = face_face_connectivity
        self.face_edge_connectivity = face_edge_connectivity

        self.edge_face_connectivity = edge_face_connectivity
        self.edge_orientation = edge_orientation

        self.edge_coordinates = edge_coordinates
        self.face_coordinates = face_coordinates
        self.boundary_coordinates = boundary_coordinates

        self.mesh_name = mesh_name

    @property
    def info(self):
        """
        summary of information about the grid
        """
        msg = ["UGrid object:"]

        msg.append("Number of nodes: %i" % len(self.nodes))
        msg.append(
            "Number of faces: %i with %i vertices per face"
            % (len(self.faces), self.num_vertices)
        )
        if self.boundaries is not None:
            msg.append("Number of boundaries: %i" % len(self.boundaries))

        # if self._data:
        #     msg.append("Variables: " + ", ".join([str(v) for v in self._data.keys()]))
        return "\n".join(msg)

    @property
    def num_vertices(self):
        """
        Maximum number of vertices in a face.

        """
        if self._faces is None:
            return None
        else:
            return self._faces.shape[1]

    @property
    def nodes(self):
        return self._nodes

    @property
    def node_lon(self):
        return self._nodes[:, 0]

    @property
    def node_lat(self):
        return self._nodes[:, 1]

    @nodes.setter  # type: ignore[no-redef]
    def nodes(self, nodes_coords):
        # Room here to do consistency checking, etc.
        # For now -- simply make sure it's a numpy array.
        if nodes_coords is None:
            self.nodes = np.zeros((0, 2), dtype=NODE_DT)
        else:
            self._nodes = np.asanyarray(nodes_coords, dtype=NODE_DT)

    @nodes.deleter  # type: ignore[no-redef]
    def nodes(self):
        # If there are no nodes, there can't be anything else.
        self._nodes = np.zeros((0, 2), dtype=NODE_DT)
        self._edges = None
        self._faces = None
        self._boundaries = None

    @property
    def faces(self):
        return self._faces

    @faces.setter
    def faces(self, faces_indexes):
        # Room here to do consistency checking, etc.
        # For now -- simply make sure it's a numpy array.
        if faces_indexes is not None:
            self._faces = np.asanyarray(faces_indexes, dtype=IND_DT)
        else:
            self._faces = None
            # Other things are no longer valid.
            self._face_face_connectivity = None
            self._face_edge_connectivity = None

    @faces.deleter
    def faces(self):
        self._faces = None
        self._faces = None
        # Other things are no longer valid.
        self._face_face_connectivity = None
        self._face_edge_connectivity = None
        self.edge_coordinates = None

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges_indexes):
        # Room here to do consistency checking, etc.
        # For now -- simply make sure it's a numpy array.
        if edges_indexes is not None:
            self._edges = np.asanyarray(edges_indexes, dtype=IND_DT)
        else:
            self._edges = None
            self._face_edge_connectivity = None

    @edges.deleter
    def edges(self):
        self._edges = None
        self._face_edge_connectivity = None
        self.edge_coordinates = None

    @property
    def boundaries(self):
        return self._boundaries

    @boundaries.setter
    def boundaries(self, boundaries_indexes):
        # Room here to do consistency checking, etc.
        # For now -- simply make sure it's a numpy array.
        if boundaries_indexes is not None:
            self._boundaries = np.asanyarray(boundaries_indexes, dtype=IND_DT)
        else:
            self._boundaries = None

    @boundaries.deleter
    def boundaries(self):
        self._boundaries = None
        self.boundary_coordinates = None

    @property
    def face_face_connectivity(self):
        return self._face_face_connectivity

    @face_face_connectivity.setter
    def face_face_connectivity(self, face_face_connectivity):
        # Add more checking?
        if face_face_connectivity is not None:
            face_face_connectivity = np.asanyarray(
                face_face_connectivity, dtype=IND_DT
            )
            if face_face_connectivity.shape != (
                len(self.faces),
                self.num_vertices,
            ):
                msg = (
                    "face_face_connectivity must be size " "(num_faces, {})"
                ).format
                raise ValueError(msg(self.num_vertices))
        self._face_face_connectivity = face_face_connectivity

    @face_face_connectivity.deleter
    def face_face_connectivity(self):
        self._face_face_connectivity = None

    @property
    def face_edge_connectivity(self):
        return self._face_edge_connectivity

    @face_edge_connectivity.setter
    def face_edge_connectivity(self, face_edge_connectivity):
        # Add more checking?
        if face_edge_connectivity is not None:
            face_edge_connectivity = np.asanyarray(
                face_edge_connectivity, dtype=IND_DT
            )
            if face_edge_connectivity.shape != (
                len(self.faces),
                self.num_vertices,
            ):
                msg = (
                    "face_face_connectivity must be size " "(num_face, {})"
                ).format
                raise ValueError(msg(self.num_vertices))
        self._face_edge_connectivity = face_edge_connectivity

    @face_edge_connectivity.deleter
    def face_edge_connectivity(self):
        self._face_edge_connectivity = None

    def infer_location(self, data, axis=-1):
        """
        :param data:
        :param axis:

        :returns: 'nodes' if data will fit to the nodes,
                  'faces' if the data will fit to the faces,
                  'boundaries' if the data will fit the boundaries.
                  None otherwise.

        If data is a netcdf variable, the "location" attribute is checked.
        """
        # We should never be calling infer_locations if it was already defined
        # try:
        #     loc = data.location
        #     if loc == "face":
        #         # FIXME: should we check the array size in this case?
        #         return "face"
        # except AttributeError:
        #     pass # try checking array size
        # # fixme: should use UGRID compliant nc_attributes if possible
        try:
            size = data.shape[axis]
        except IndexError:
            return None  # Variable has a size-zero data array
        if size == self.nodes.shape[0]:
            return "node"
        if self.faces is not None and size == self.faces.shape[0]:
            return "face"
        if self.boundaries is not None and size == self.boundaries.shape[0]:
            return "boundary"
        return None

    def build_face_face_connectivity(self):
        """
        Builds the face_face_connectivity array: giving the neighbors of each cell.

        Note: arbitrary order and CW vs CCW may not be consistent.
        """

        num_vertices = self.num_vertices
        num_faces = self.faces.shape[0]
        face_face = np.zeros((num_faces, num_vertices), dtype=IND_DT)
        face_face += -1  # Fill with -1.

        # Loop through all the faces to find the matching edges:
        edges = {}  # dict to store the edges.
        for i, face in enumerate(self.faces):
            # Loop through edges of the cell:
            for j in range(num_vertices):
                if j < self.num_vertices - 1:
                    edge = (face[j], face[j + 1])
                else:
                    edge = (face[-1], face[0])
                if edge[0] > edge[1]:  # Sort the node numbers.
                    edge = (edge[1], edge[0])
                # see if it is already in there
                prev_edge = edges.pop(edge, None)
                if prev_edge is not None:
                    face_num, edge_num = prev_edge
                    face_face[i, j] = face_num
                    face_face[face_num, edge_num] = i
                else:
                    edges[edge] = (i, j)  # face num, edge_num.
        self._face_face_connectivity = face_face

    def get_lines(self):
        if self.edges is None:
            self.build_edges()
        return self.nodes[self.edges]

    def build_edges(self):
        """
        Builds the edges array: all the edges defined by the faces

        This will replace the existing edge array, if there is one.

        NOTE: arbitrary order -- should the order be preserved?
        """
        if self.faces is None:
            # No faces means no edges
            self._edges = None
            return

        faces = self.faces

        is_masked = np.ma.isMA(faces)
        if is_masked:
            first = faces.copy()
            first[:] = faces[:, :1]
            save_mask = faces.mask.copy()
            faces[save_mask] = first.data[faces.mask]

        face_edges = np.dstack([faces, np.roll(faces, 1, 1)])

        if is_masked and np.ndim(save_mask):
            face_edges.mask = np.dstack(
                [np.zeros_like(save_mask), np.roll(save_mask, 1, 1)]
            )

        face_edges.sort(axis=-1)

        all_edges = face_edges.reshape((-1, 2))

        if is_masked and np.ndim(save_mask):
            edges = np.unique(all_edges[~all_edges.mask.any(axis=-1)], axis=0)
        else:
            edges = np.unique(all_edges, axis=0)
        self._edges = edges

    def build_boundaries(self):
        """
        Builds the boundary segments from the cell array.

        It is assumed that -1 means no neighbor, which indicates a boundary

        This will over-write the existing boundaries array if there is one.

        This is a not-very-smart just loop through all the faces method.

        """
        boundaries = []
        for i, face in enumerate(self.face_face_connectivity):
            for j, neighbor in enumerate(face):
                if neighbor == -1:
                    if j == self.num_vertices - 1:
                        bound = (self.faces[i, -1], self.faces[i, 0])
                    else:
                        bound = (self.faces[i, j], self.faces[i, j + 1])
                    boundaries.append(bound)
        self.boundaries = boundaries

    def build_face_edge_connectivity(self):
        """
        Builds the face-edge connectivity array
        """
        self.face_edge_connectivity = self._build_face_edge_connectivity()

    def _build_face_edge_connectivity(self, sort=True):
        try:
            from scipy.spatial import cKDTree
        except ImportError:
            raise ImportError(
                "The scipy package is required to use "
                "UGrid.build_face_edge_connectivity"
            )

        faces = self.faces.copy()
        if self.edges is None:
            self.build_edges()
        edges = self.edges.copy()

        is_masked = np.ma.isMA(faces)
        if is_masked:
            first = faces.copy()
            first[:] = faces[:, :1]
            save_mask = faces.mask.copy()
            faces[save_mask] = first.data[faces.mask]

        face_edges = np.dstack([faces, np.roll(faces, 1, 1)])

        if is_masked and np.ndim(save_mask):
            face_edges.mask = np.dstack(
                [np.zeros_like(save_mask), np.roll(save_mask, 1, 1)]
            )

        if sort:
            face_edges.sort(axis=-1)
            edges.sort(axis=-1)

        tree = cKDTree(edges)

        face_edge_2d = face_edges.reshape((-1, 2))

        if is_masked and save_mask.any():
            mask = face_edge_2d.mask.any(-1)
            connectivity = np.ma.ones(
                len(face_edge_2d),
                dtype=face_edge_2d.dtype,
            )
            connectivity.mask = mask
            connectivity[~mask] = tree.query(
                face_edge_2d[~mask], distance_upper_bound=0.1
            )[1]
        else:
            connectivity = tree.query(face_edge_2d, distance_upper_bound=0.1)[
                1
            ]
        return np.roll(connectivity.reshape(faces.shape), -1, -1)

    def get_face_edge_orientation(self):
        """
        Get the orientation for each edge in the corresponding face

        This method returns an array with the same shape as :attr:`faces` that
        is one if the corresponding edge has the same orientation as in
        :attr:`edges`, and -1 otherwise
        """
        # we build the face edge connectivity but do not sort the edge nodes.
        # With this, we will get `num_edges` where the edge is flipped compared
        # to the definition in :attr:`edges`
        face_edge_connectivity = self._build_face_edge_connectivity(sort=False)
        num_edges = self.edges.shape[0]
        if np.ma.isMA(face_edge_connectivity):
            return np.ma.where(face_edge_connectivity == num_edges, 1, -1)
        else:
            return np.where(face_edge_connectivity == num_edges, 1, -1)

    def build_edge_face_connectivity(self):
        """Build the edge_face_connectivity

        The edge_face_connectivity is the mapping from each edge in the
        :attr:`edges` to the attached face in `faces`.
        """
        if self.face_edge_connectivity is None:
            self.build_face_edge_connectivity()
        face_edge_connectivity = self.face_edge_connectivity
        orientation = self.get_face_edge_orientation()

        n_edge = fill_value = len(self.edges)
        n_face = len(self.faces)

        if np.ma.isMA(face_edge_connectivity):
            face_edge_connectivity = face_edge_connectivity.filled(fill_value)

        n_face, nmax_edge = face_edge_connectivity.shape
        # Get rid of the fill_value, create a 1:1 mapping between faces and edges
        isnode = (face_edge_connectivity != fill_value).ravel()
        face_index = np.repeat(np.arange(n_face), nmax_edge).ravel()[isnode]
        orientation_nodes = orientation.ravel()[isnode]
        edge_index = face_edge_connectivity.ravel()[isnode]

        # We know that every edge will have either one or two associated faces
        isface = np.empty((n_edge, 2), dtype=bool)
        isface[:, 0] = True
        isface[:, 1] = np.bincount(edge_index) == 2

        # Allocate the output array
        edge_face_connectivity = np.full((n_edge, 2), n_face, dtype=np.int64)
        # Invert the face_index, and use the boolean array to place them appropriately
        edge_face_connectivity.ravel()[isface.ravel()] = face_index[
            np.argsort(edge_index)
        ]
        self.edge_face_connectivity = np.ma.masked_where(
            edge_face_connectivity == n_face, edge_face_connectivity
        )

        edge_orientation = np.full((n_edge, 2), -999, dtype=np.int64)
        # Invert the face_index, and use the boolean array to place them appropriately
        edge_orientation.ravel()[isface.ravel()] = orientation_nodes[
            np.argsort(edge_index)
        ]
        self.edge_orientation = np.ma.masked_where(
            edge_orientation == -999, edge_orientation
        )

    def _get_node_edge_connectivity_unsorted(self):
        """Build the node_edge_connectivity.

        The node_edge_connectivity is the mapping from each node in the
        :attr:`nodes` to the attached edge in :attr:`edges`. Note that this
        method does not sort the edges so they are in general not in
        anti-clockwise order.
        """
        if self.edges is None:
            self.build_edges()
        edge_node_connectivity = self.edges

        n_edge = len(self.edges)
        n_edge, nmax_node = edge_node_connectivity.shape
        n_node = fill_value = len(self.nodes)

        if np.ma.isMA(edge_node_connectivity):
            edge_node_connectivity = edge_node_connectivity.filled(fill_value)

        # Get rid of the fill_value, create a 1:1 mapping between edges and
        # nodes
        isnode = (edge_node_connectivity != fill_value).ravel()
        edge_index = np.repeat(np.arange(n_edge), nmax_node).ravel()[isnode]
        node_index = edge_node_connectivity.ravel()[isnode]

        node_counts = np.bincount(node_index)
        nmax_edge = node_counts.max()

        # We know that every edge will have either one or two associated faces
        isedge = np.empty((n_node, nmax_edge), dtype=bool)
        for i in range(nmax_edge):
            isedge[:, i] = node_counts > i

        # Allocate the output array
        node_edge_connectivity = np.full(
            (n_node, nmax_edge), n_edge, dtype=np.int64
        )
        # Invert the face_index, and use the boolean array to place them
        # appropriately
        node_edge_connectivity.ravel()[isedge.ravel()] = edge_index[
            np.argsort(node_index)
        ]
        return np.ma.masked_where(
            node_edge_connectivity == n_edge, node_edge_connectivity
        )

    def _create_dual_edge_mesh(self):
        """Create a :class:`UGrid` instance that represents the dual edge mesh."""
        if self.face_edge_connectivity is None:
            self.build_face_edge_connectivity()

        edges = self.edges

        if self.edge_face_connectivity is None:
            self.build_edge_face_connectivity()

        n_face = len(self.faces)
        n_node = len(self.nodes)

        edge_face_connectivity = self.edge_face_connectivity.filled(n_face)

        # now get the orientation for each edge from the `orientation` array
        mask = edge_face_connectivity < n_face
        edge_orientation = self.edge_orientation.filled(-999)

        # use num_faces as fill value (necessary for edges at the domain boundary)
        dual_face_node_connectivity = np.full(
            (len(edges), 4), -999, dtype=self.edges.dtype
        )
        dual_face_node_connectivity[:, 0] = edges[:, 0]
        dual_face_node_connectivity[:, 2] = edges[:, 1]

        # get the first index for the face center nodes
        if self.face_coordinates is None:
            self.build_face_coordinates()

        dual_nodes = np.r_[self.nodes, self.face_coordinates]

        # now handle the case where the orientation is -1. This should be at
        # dual_face_node_connectivity[:, 1]
        mask = edge_orientation == -1
        dual_face_node_connectivity[mask.any(axis=-1), 3] = (
            edge_face_connectivity[mask] + n_node
        )

        # the same for +1, should be at dual_face_node_connectivity[:, 3]
        mask = edge_orientation == 1
        dual_face_node_connectivity[mask.any(axis=-1), 1] = (
            edge_face_connectivity[mask] + n_node
        )

        # now we need to roll where dual_face_node_connectivity[:, 1] == -999
        # to make sure that the fill values are at the end
        roll_at = dual_face_node_connectivity[:, 1] == -999
        dual_face_node_connectivity[roll_at] = np.roll(
            dual_face_node_connectivity[roll_at], 2, axis=1
        )

        # now turn dual_face_node_connectivity into a masked array
        # NOTE: There is no definititive policy yet how to deal with fill
        # values within the gridded package, see
        # https://github.com/NOAA-ORR-ERD/gridded/pull/60#issuecomment-744810919
        dual_face_node_connectivity = np.ma.masked_where(
            dual_face_node_connectivity == -999, dual_face_node_connectivity
        )

        return dual_face_node_connectivity.astype(int), dual_nodes

    def _create_dual_node_mesh(self):
        """Create the dual mesh for the nodes."""
        from psy_ugrid._create_dual_node_mesh import get_face_node_connectivity

        (
            dual_edge_face_node_connectivity,
            dual_nodes,
        ) = self._create_dual_edge_mesh()

        # create a node_edge_connectivty
        node_edge_connectivity = self._get_node_edge_connectivity_unsorted()

        if self.edge_coordinates is None:
            self.build_edge_coordinates()

        edge_coordinates = self.edge_coordinates

        n_edge = len(self.edges)
        n_node = len(self.nodes)
        n_dual_node = len(dual_nodes)
        n_dual_node_max = n_dual_node + n_edge

        face_node_connectivity = self.faces
        if np.ma.isMA(face_node_connectivity):
            face_node_connectivity = face_node_connectivity.filled(
                len(self.nodes)
            )
        nmax_face = (
            np.bincount(
                face_node_connectivity[face_node_connectivity < n_node]
            ).max()
            + 3
        )

        node_edge_connectivity = node_edge_connectivity.filled(n_edge)
        dual_edge_face_node_connectivity = (
            dual_edge_face_node_connectivity.filled(n_dual_node_max)
        )

        dual_node_face_node_connectivity = np.full(
            (n_node, nmax_face), int(n_dual_node_max), dtype=np.int64
        )

        dual_node_face_node_connectivity = np.asarray(
            get_face_node_connectivity(
                dual_edge_face_node_connectivity,
                node_edge_connectivity,
                n_dual_node,
                nmax_face,
            )
        )

        is_new_node = dual_node_face_node_connectivity >= n_dual_node
        all_new = dual_node_face_node_connectivity[is_new_node]
        new_nodes = np.unique(dual_node_face_node_connectivity[is_new_node])

        dual_node_face_node_connectivity[
            is_new_node
        ] = n_dual_node + new_nodes.searchsorted(all_new)
        n_dual_node_max = n_dual_node + len(new_nodes) - 1

        return (
            np.ma.masked_where(
                dual_node_face_node_connectivity == n_dual_node_max,
                dual_node_face_node_connectivity,
            ),
            np.r_[dual_nodes, edge_coordinates[new_nodes[:-1] - n_dual_node]],
        )

    def create_dual_mesh(self, location="edge"):
        """Create the dual mesh for edge or nodes.

        This method creates the dual mesh, either specified through the nodes,
        or specified through the edges. For a Delaunay triangulation case with
        ``location == "node"``, this is commonly known as Voronoi Polygons.

        :param location="edge" : the source for the dual mash. can be one of
                                 ``"node"`` or ``"edge"``
        :type location: str

        :returns: A :class:`UGrid` with `nodes` and `faces` of the dual mesh.
        """
        if location == "edge":
            face_node_connectivity, nodes = self._create_dual_edge_mesh()
        elif location == "node":
            face_node_connectivity, nodes = self._create_dual_node_mesh()
        else:
            raise ValueError(
                "location must be `edge` or `node`, found `%s`" % (location,)
            )
        if self.mesh_name:
            mesh_name = self.mesh_name + "_dual_" + location
        else:
            mesh_name = "dual_" + location
        return UGrid(nodes, faces=face_node_connectivity, mesh_name=mesh_name)

    def build_face_coordinates(self):
        """
        Builds the face_coordinates array, using the average of the
        nodes defining each face.

        Note that you may want a different definition of the face
        coordinates than this computes, but this is here to have
        an easy default.

        This will write-over an existing face_coordinates array.

        Useful if you want this in the output file.

        """
        faces = self.faces
        if not np.ma.isMA(faces) or not np.ndim(faces.mask):
            self.face_coordinates = self.nodes[faces].mean(axis=1)
        else:
            mask = np.dstack([faces.mask, faces.mask])
            coords = self.nodes[faces.filled(0)]
            coords[mask] = np.nan
            self.face_coordinates = np.nanmean(coords, axis=1)

    def build_edge_coordinates(self):
        """
        Builds the edge_coordinates array, using the average of the
        nodes defining each edge.

        Note that you may want a different definition of the edge
        coordinates than this computes, but this is here to have
        an easy default.


        This will write-over an existing edge_coordinates array

        Useful if you want this in the output file

        """
        self.edge_coordinates = self.nodes[self.edges].mean(axis=1)

    def build_boundary_coordinates(self):
        """
        Builds the boundary_coordinates array, using the average of the
        nodes defining each boundary segment.

        Note that you may want a different definition of the boundary
        coordinates than this computes, but this is here to have
        an easy default.

        This will write-over an existing face_coordinates array

        Useful if you want this in the output file

        """
        boundary_coordinates = np.zeros(
            (len(self.boundaries), 2), dtype=NODE_DT
        )
        # FXIME: there has got to be a way to vectorize this.
        for i, bound in enumerate(self.boundaries):
            coords = self.nodes[bound]
            boundary_coordinates[i] = coords.mean(axis=0)
        self.boundary_coordinates = boundary_coordinates
