r"""``sphobjinv`` *package definition module*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    17 May 2016

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

__all__ = [
    "readbytes",
    "writebytes",
    "readjson",
    "writejson",
    "urlwalk",
    "compress",
    "decompress",
    "pb_comments",
    "pb_data",
    "pb_version",
    "pb_project",
    "p_data",
    "DataFields",
    "HeaderFields",
    "SourceTypes",
    "SphobjinvError",
    "VersionError",
    "DataObjStr",
    "DataObjBytes",
    "Inventory",
    "json_schema",
]

from sphobjinv.data import DataObjStr, DataObjBytes, DataFields
from sphobjinv.inventory import Inventory, SourceTypes, HeaderFields
from sphobjinv.error import SphobjinvError, VersionError
from sphobjinv.fileops import readbytes, writebytes, readjson, writejson, urlwalk
from sphobjinv.re import pb_comments, pb_data, pb_version, pb_project
from sphobjinv.re import p_data
from sphobjinv.schema import json_schema
from sphobjinv.version import __version__  # noqa: F401
from sphobjinv.zlib import compress, decompress
