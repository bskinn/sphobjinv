# ----------------------------------------------------------------------------
# Name:        fileops
# Purpose:     File operations for sphobjinv
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

"""Disk I/O module for sphobjinv."""


def readbytes(path):
    """Read file contents and return as bytes.

    Parameters
    ----------
    path

        |str| -- Path to file to be opened.

    Returns
    -------
    b

        |bytes| -- Binary contents of the indicated file.

    """
    # Open the file and read
    with open(path, 'rb') as f:
        return f.read()


def writebytes(path, contents):
    """Write indicated file contents (with clobber).

    Parameters
    ----------
    path

        |str| -- Path to file to be written.

    contents

        |bytes| -- Binary string of data to be written to file.


    """
    # Open the file and write
    with open(path, 'wb') as f:
        f.write(contents)


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
