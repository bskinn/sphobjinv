r"""*CLI module for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

.. note::

    This module is NOT part of the public API for ``sphobjinv``.
    Its entire contents should be considered implementation detail.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    17 May 2016

**Copyright**
    \(c) Brian Skinn 2016-2020

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import argparse as ap
import json
import os
import sys
from json.decoder import JSONDecodeError
from urllib.error import HTTPError, URLError

from jsonschema.exceptions import ValidationError

from sphobjinv import __version__
from sphobjinv.error import VersionError
from sphobjinv.fileops import readjson, urlwalk, writebytes, writejson
from sphobjinv.inventory import Inventory as Inv
from sphobjinv.zlib import compress
