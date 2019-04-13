r"""*Helper module to retrieve resource .inv files for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    12 Apr 2019

**Copyright**
    \(c) Brian Skinn 2016-2019

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from pathlib import Path

testall_inv_paths = list(
    p
    for p in (Path(__file__).parent / "resource").iterdir()
    if p.name.startswith("objects_") and p.name.endswith(".inv")
)
