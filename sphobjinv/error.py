# ----------------------------------------------------------------------------
# Name:        error
# Purpose:     Custom errors for sphobjinv
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

"""Module defining errors for sphobjinv."""


class SphobjinvError(Exception):
    """Exception superclass for the project."""


class VersionError(SphobjinvError):
    """Attempting an operation on an unsupported version."""


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
