# ----------------------------------------------------------------------------
# Name:        re
# Purpose:     Helper regexes for sphobjinv
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     5 Nov 2017
# Copyright:   (c) Brian Skinn 2016-2018
# License:     The MIT License; see "LICENSE.txt" for full license terms
#                   and contributor agreement.
#
#       This file is part of Sphinx Objects.inv Encoder/Decoder, a toolkit for
#       encoding and decoding objects.inv files for use with intersphinx.
#
#       http://www.github.com/bskinn/sphobjinv
#
# ----------------------------------------------------------------------------

"""Module with helper regexes for sphobjinv."""

import re

from .data import DataFields
from .inventory import HeaderFields


#: Bytestring regex pattern for comment lines in decompressed
#: ``objects.inv`` files
pb_comments = re.compile(b'^#.*$', re.M)

#: Bytestring regex pattern for project line
pb_project = re.compile("""
    ^                        # Start of line
    [#][ ]Project:[ ]        # Preamble
    (?P<{}>.+?)              # Lazy rest of line is the project name
    \\r?$                    # Ignore possible CR at EOL
    """.format(HeaderFields.Project.value).encode(encoding='utf-8'),
                       re.M | re.X)

#: Bytestring regex pattern for version line
pb_version = re.compile("""
    ^                        # Start of line
    [#][ ]Version:[ ]        # Preamble
    (?P<{}>.+?)              # Lazy rest of line is the version
    \\r?$                    # Ignore possible CR at EOL
    """.format(HeaderFields.Version.value).encode(encoding='utf-8'),
                       re.M | re.X)

#: Regex pattern for compilation into str and bytes re patterns
ptn_data = """\
    ^                        # Start of line
    (?P<{0}>[^#]\\S+)        # --> Name
    \\s+                     # Dividing space
    (?P<{1}>\\w+)            # --> Domain
    :                        # Dividing colon
    (?P<{2}>\\w+)            # --> Role
    \\s+                     # Dividing space
    (?P<{3}>-?\\d+)          # --> Priority
    \\s+                     # Dividing space
    (?P<{4}>\\S+)            # --> URI
    \\s+                     # Dividing space
    (?P<{5}>.+?)             # --> Display name, lazy b/c possible CR
    \\r?$                    # Ignore possible CR at EOL
    """.format(DataFields.Name.value,
               DataFields.Domain.value,
               DataFields.Role.value,
               DataFields.Priority.value,
               DataFields.URI.value,
               DataFields.DispName.value)

#: Bytestring regex pattern for bytes data lines in decompressed
#: ``objects.inv`` files
pb_data = re.compile(ptn_data.encode(encoding='utf-8'), re.M | re.X)

#: str regex pattern for str data lines in decompressed
#: ``objects.inv`` files
p_data = re.compile(ptn_data, re.M | re.X)

if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
