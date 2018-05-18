r"""``sphobjinv`` *package definition module*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    17 May 2016

**Copyright**
    \(c) Brian Skinn 2016-2018

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from __future__ import absolute_import

__all__ = ['readbytes', 'writebytes', 'readjson', 'writejson',
           'compress', 'decompress',
           'pb_comments', 'pb_data', 'pb_version', 'pb_project',
           'p_data',
           'DataFields', 'HeaderFields',
           'SourceTypes',
           'SphobjinvError', 'VersionError',
           'DataObjStr', 'DataObjBytes',
           'Inventory',
           'json_schema']

from .data import DataObjStr, DataObjBytes, DataFields
from .inventory import Inventory, SourceTypes, HeaderFields
from .error import SphobjinvError, VersionError
from .fileops import readbytes, writebytes, readjson, writejson
from .re import pb_comments, pb_data, pb_version, pb_project
from .re import p_data
from .schema import json_schema
from .zlib import compress, decompress


__version__ = '2.0rc1'
