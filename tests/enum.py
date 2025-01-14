r"""
Separate :class:`enum.Enum` from ``conftest.py``.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    14 Jan 2025

**Copyright**
    \(c) Brian Skinn 2016-2024

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

**Members**

"""

import enum


class Entrypoints(enum.Enum):
    """Entrypoints."""

    SOI = "sphobjinv"
    SOI_TEXTCONV = "sphobjinv-textconv"
