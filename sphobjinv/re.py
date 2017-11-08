# ----------------------------------------------------------------------------
# Name:        re
# Purpose:     Helper regexes for sphobjinv
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     5 Nov 2017
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

"""Module with helper regexes for sphobjinv."""

from enum import Enum
import re


class DataFields(Enum):
    """Enum for the regex groups of objects.inv data items."""

    Name = 'name'
    Domain = 'domain'
    Role = 'role'
    Priority = 'priority'
    URI = 'uri'
    DispName = 'dispname'


class HeaderFields(Enum):
    """Enum for regex groups of objects.inv header data."""

    Project = 'project'
    Version = 'version'


#: Bytestring regex pattern for comment lines in decoded
#: ``objects.inv`` files
p_comments = re.compile(b'^#.*$', re.M)

#: Bytestring regex pattern for project line
p_project = re.compile("""
    ^                        # Start of line
    [#][ ]Project:[ ]        # Preamble
    (?P<{}>.+)               # Rest of line is the project name
    $                        # EOL
    """.format(HeaderFields.Project.value).encode(encoding='utf-8'),
                       re.M | re.X)

#: Bytestring regex pattern for version line
p_version = re.compile("""
    ^                        # Start of line
    [#][ ]Version:[ ]        # Preamble
    (?P<{}>.+)               # Rest of line is the version
    $                        # EOL
    """.format(HeaderFields.Version.value).encode(encoding='utf-8'),
                       re.M | re.X)

#: Bytestring regex pattern for data lines in decoded
#: ``objects.inv`` files
p_data = re.compile("""\
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
    (?P<{5}>.+)              # --> Display name
    $                        # Possible space to end of line
    """.format(DataFields.Name.value,
               DataFields.Domain.value,
               DataFields.Role.value,
               DataFields.Priority.value,
               DataFields.URI.value,
               DataFields.DispName.value).encode(encoding='utf-8'),
                    re.M | re.X)


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
