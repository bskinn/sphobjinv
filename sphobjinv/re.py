# ----------------------------------------------------------------------------
# Name:        regex
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

import re


#: Bytestring regex pattern for comment lines in decoded
#: ``objects.inv`` files
p_comments = re.compile(b'^#.*$', re.M)

#: Bytestring regex pattern for data lines in decoded
#: ``objects.inv`` files
p_data = re.compile(b'^[^#].*$', re.M)


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
