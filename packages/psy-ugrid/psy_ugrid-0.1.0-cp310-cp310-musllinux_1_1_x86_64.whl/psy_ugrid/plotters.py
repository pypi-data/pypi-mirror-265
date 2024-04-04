# SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: LGPL-3.0-only

"""plotters module of the psy-ugrid psyplot plugin

This module defines the plotters for the psy-ugrid
package. It should import all requirements and define the formatoptions and
plotters that are specified in the
:mod:`psy_ugrid.plugin` module.
"""

from psyplot.plotter import Formatoption, Plotter

# -----------------------------------------------------------------------------
# ---------------------------- Formatoptions ----------------------------------
# -----------------------------------------------------------------------------


class MyNewFormatoption(Formatoption):
    def update(self, value):
        # hooray
        pass


# -----------------------------------------------------------------------------
# ------------------------------ Plotters -------------------------------------
# -----------------------------------------------------------------------------


class MyPlotter(Plotter):
    _rcparams_string = ["plotter.psy_ugrid."]

    my_fmt = MyNewFormatoption("my_fmt")
