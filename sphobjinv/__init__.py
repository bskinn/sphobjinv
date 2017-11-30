# ----------------------------------------------------------------------------
# Name:        __init__
# Purpose:     Package definition module for sphobjinv
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     17 May 2016
# Copyright:   (c) Brian Skinn 2016-2017
# License:     The MIT License; see "LICENSE.txt" for full license terms
#                   and contributor agreement.
#
#       This file is part of Sphinx Objects.inv Encoder/Decoder, a toolkit for
#       encoding and decoding objects.inv files for use with intersphinx.
#
#       http://www.github.com/bskinn/sphobjinv
#
# ----------------------------------------------------------------------------


"""Definition file for root of sphobjinv."""


from __future__ import absolute_import

__all__ = ['readfile', 'writefile',
           'encode', 'decode',
           'pb_comments', 'pb_data', 'pb_version', 'pb_project',
           'p_data',
           'DataFields', 'HeaderFields',
           'SphobjinvError', 'VersionError',
           'DataObjStr', 'DataObjBytes',
           'Inventory']

from .data import DataObjStr, DataObjBytes
from .data import DataFields, HeaderFields
from .data import Inventory
from .error import SphobjinvError, VersionError
from .fileops import readfile, writefile
from .re import pb_comments, pb_data, pb_version, pb_project
from .re import p_data
from .zlib import decode, encode


__version__ = '2.0.dev1'
