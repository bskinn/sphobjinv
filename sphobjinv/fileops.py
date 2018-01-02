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


def readfile(path, cmdline=False):
    """Read file contents and return as binary string.

    Parameters
    ----------
    path

        |str| -- Path to file to be opened.

    cmdline

        |bool| -- If |False|, exceptions are raised as normal.
        If |True|, on raise of any subclass of :class:`Exception`,
        the function returns |None|.

    Returns
    -------
    b

        |bytes| -- Binary contents of the indicated file.

    """
    # Open the file and read
    try:
        with open(path, 'rb') as f:
            b = f.read()
    except Exception:
        if cmdline:
            b = None
        else:
            raise

    # Return the result
    return b


def writefile(path, contents, cmdline=False):
    """Write indicated file contents (with clobber).

    Parameters
    ----------
    path

        |str| -- Path to file to be written.

    contents

        |bytes| -- Binary string of data to be written to file.

    cmdline

        |bool| -- If |False|, exceptions are raised as normal.
        If |True|, on raise of any subclass of :class:`Exception`,
        the function returns |None|.

    Returns
    -------
    p

        |str| -- If write is successful, echo of the `path` input |str| is
        returned.  If any :class:`Exception` is raised and `cmdline` is
        |True|, |None| is returned.

    """
    # Open the file and write
    try:
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        if cmdline:
            return None
        else:
            raise

    return path


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
