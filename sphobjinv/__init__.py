#-------------------------------------------------------------------------------
# Name:        __init__
# Purpose:     Package definition module for sphobjinv
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     17 May 2016
# Copyright:   (c) Brian Skinn 2016
# License:     The MIT License; see "license.txt" for full license terms
#                   and contributor agreement.
#
#       This file is part of Sphinx Objects.inv Encoder/Decoder, a toolkit for
#       encoding and decoding objects.inv files for use with intersphinx.
#
#       http://www.github.com/bskinn/sphobjinv
#
#-------------------------------------------------------------------------------

from __future__ import absolute_import

from .sphobjinv import readfile, writefile, decode, encode
from .sphobjinv import p_comments, p_data

__version__ = '1.0'

