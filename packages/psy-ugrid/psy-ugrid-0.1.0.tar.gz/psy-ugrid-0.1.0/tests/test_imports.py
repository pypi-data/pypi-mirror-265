# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: LGPL-3.0-only

"""Test file for imports."""


def test_package_import():
    """Test the import of the main package."""
    import psy_ugrid  # noqa: F401
    import psy_ugrid._create_dual_node_mesh  # noqa: F401
