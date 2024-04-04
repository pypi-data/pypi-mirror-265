<!--
SPDX-FileCopyrightText: 2024 Helmholtz-Zentrum hereon GmbH

SPDX-License-Identifier: CC-BY-4.0
-->

# psy-ugrid

[![CI](https://codebase.helmholtz.cloud/psyplot/psy-ugrid/badges/main/pipeline.svg)](https://codebase.helmholtz.cloud/psyplot/psy-ugrid/-/pipelines?page=1&scope=all&ref=main)
[![Code coverage](https://codebase.helmholtz.cloud/psyplot/psy-ugrid/badges/main/coverage.svg)](https://codebase.helmholtz.cloud/psyplot/psy-ugrid/-/graphs/main/charts)
[![Latest Release](https://codebase.helmholtz.cloud/psyplot/psy-ugrid/-/badges/release.svg)](https://codebase.helmholtz.cloud/psyplot/psy-ugrid)
[![PyPI version](https://img.shields.io/pypi/v/psy-ugrid.svg)](https://pypi.python.org/pypi/psy-ugrid/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![REUSE status](https://api.reuse.software/badge/codebase.helmholtz.cloud/psyplot/psy-ugrid)](https://api.reuse.software/info/codebase.helmholtz.cloud/psyplot/psy-ugrid)


A psyplot plugin for decoding unstructured grids following the UGRID conventions

## Installation

Install this package in a dedicated python environment via

```bash
python -m venv venv
source venv/bin/activate
pip install psy-ugrid
```

To use this in a development setup, clone the [source code][source code] from
gitlab, start the development server and make your changes::

```bash
git clone https://codebase.helmholtz.cloud/psyplot/psy-ugrid
cd psy-ugrid
python -m venv venv
source venv/bin/activate
make dev-install
```

More detailed installation instructions my be found in the [docs][docs].


[source code]: https://codebase.helmholtz.cloud/psyplot/psy-ugrid
[docs]: https://psyplot.github.io/psy-ugrid/installation.html

## Usage

Once installed, the `UGRIDDecoder` is automatically registered within the
`psyplot` framework. Once you open a UGRID-conform file, the `UGRIDDecoder`
will be automatically used for all variables in the netCDF-file that define a
`mesh`. You do not have to do anything extra.

A :ref:`demo` on how this package works can be found [in the docs][docs].


## Technical note

This package has been generated from the template
https://codebase.helmholtz.cloud/psyplot/psyplot-plugin-template.git.

See the template repository for instructions on how to update the skeleton for
this package.


## License information

Copyright © 2024 Helmholtz-Zentrum hereon GmbH



Code files in this repository are licensed under the
LGPL-3.0-only, if not stated otherwise
in the file.

Documentation files in this repository are licensed under CC-BY-4.0, if not stated otherwise in the file.

Supplementary and configuration files in this repository are licensed
under CC0-1.0, if not stated otherwise
in the file.

Please check the header of the individual files for more detailed
information.



### License management

License management is handled with [``reuse``](https://reuse.readthedocs.io/).
If you have any questions on this, please have a look into the
[contributing guide][contributing] or contact the maintainers of
`psy-ugrid`.

[contributing]: https://psyplot.github.io/psy-ugrid/contributing.html
