# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: LGPL-3.0-only

# coding: utf-8
"""Test file for building the face_edge_connectivity"""
from typing import Callable, List

import numpy as np

from psy_ugrid import ugrid


def test_create_dual_node_mesh(
    same_upon_permutation: Callable[[List, List], bool]
):
    r"""Test for a mesh like

     /|\
    /_|_\
    """
    nodex = [0, 1, 1, 2]
    nodey = [0, 1, 0, 0]
    faces = [[0, 1, 2], [2, 1, 3]]

    edges = [[0, 1], [1, 2], [2, 0], [1, 3], [2, 3]]
    grid = ugrid.UGrid(
        node_lon=nodex, node_lat=nodey, faces=faces, edges=edges
    )

    ref = [
        [4, 6, 0, 7, -999],
        [6, 4, 5, 8, 1],
        [5, 4, 7, 2, 9],
        [8, 5, 9, 3, -999],
    ]

    dual_faces, dual_nodes = grid._create_dual_node_mesh()

    # check length of nodes.
    # 4 original nodes + 2 face centers + 4 edge centers
    # (edge 1-2 does not appear)
    assert len(dual_nodes) == 10

    # check faces
    assert np.ma.isMA(dual_faces)
    test = dual_faces.filled(-999).tolist()
    tests = [same_upon_permutation(t, r) for t, r in zip(test, ref)]
    try:
        assert all(tests)
    except AssertionError:
        # for better error message
        assert test == ref


def test_create_dual_node_mesh_na(
    same_upon_permutation: Callable[[List, List], bool]
):
    r"""Test for a mesh like

    |‾|\
    |_|_\
    """
    nodex = [0, 0, 1, 1, 2]
    nodey = [0, 1, 1, 0, 0]
    faces = np.ma.array(
        [[0, 1, 2, 3], [2, 4, 3, -999]],
        mask=[[False, False, False, False], [False, False, False, True]],
    )

    edges = [[0, 1], [1, 2], [2, 3], [3, 0], [2, 4], [4, 3]]
    grid = ugrid.UGrid(
        node_lon=nodex, node_lat=nodey, faces=faces, edges=edges
    )

    ref = [
        [5, 7, 0, 9, -999],
        [7, 5, 8, 1, -999],
        [8, 5, 6, 10, 2],
        [6, 5, 9, 3, 11],
        [10, 6, 11, 4, -999],
    ]

    dual_faces, dual_nodes = grid._create_dual_node_mesh()

    # check length of nodes.
    # 5 original nodes + 2 face centers + 5 edge centers
    # (edge 2-3 does not appear)
    assert len(dual_nodes) == 12

    # check faces
    assert np.ma.isMA(dual_faces)
    test = dual_faces.filled(-999).tolist()
    tests = [same_upon_permutation(t, r) for t, r in zip(test, ref)]
    try:
        assert all(tests)
    except AssertionError:
        # for better error message
        assert test == ref
