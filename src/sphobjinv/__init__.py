r"""``sphobjinv`` *package definition module*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    17 May 2016

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


from sphobjinv.data import DataFields, DataObjBytes, DataObjStr
from sphobjinv.enum import HeaderFields, SourceTypes
from sphobjinv.error import SphobjinvError, VersionError
from sphobjinv.fileops import readbytes, readjson, urlwalk, writebytes, writejson
from sphobjinv.inventory import Inventory
from sphobjinv.re import p_data, pb_comments, pb_data, pb_project, pb_version
from sphobjinv.schema import json_schema
from sphobjinv.version import __version__
from sphobjinv.zlib import compress, decompress
