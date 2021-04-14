r"""``sphobjinv`` *package execution module*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    15 May 2020

**Copyright**
    \(c) Brian Skinn 2016-2021

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import sys

from sphobjinv.cli.core import main

if __name__ == "__main__":
    # Spoof so 'help' usage display shows "sphobjinv" and
    # not "__main__.py"
    sys.argv[0] = "sphobjinv"

    sys.exit(main())
