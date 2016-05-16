#-------------------------------------------------------------------------------
# Name:        decode
# Purpose:     Decoder script for Sphinx objects.inv files
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     16 May 2016
# Copyright:   (c) Brian Skinn 2016
# License:     The MIT License; see "license.txt" for full license terms
#                   and contributor agreement.
#
#       This file is part of sphobjinv (Sphinx-ObjectsInv), a toolkit for
#       encoding and decoding objects.inv files for use with intersphinx
#
#       http://www.github.com/bskinn/sphinvobj
#
#-------------------------------------------------------------------------------

import argparse as ap
import os
import zlib
import sys


# Set up the argparse framework
prs = ap.ArgumentParser(description="Decode intersphinx 'objects.inv' files.")

prs.add_argument('infile', help="Path to 'objects.inv' file to be decoded")
prs.add_argument('--outfile', help="Path to desired output file", default=None,
                 required=False)



def readfile(path):
    """ 'readfile' Docstring
    """

    # Open the file and read
    try:
        with open(path, 'rb') as f:
            b = f.read()
    except IOError:
        b = None

    # Return the result
    return b


if __name__ ==  '__main__':

    # Parse commandline arguments
    ns, args_left = prs.parse_known_args()
    params = vars(ns)

    # Infile path and name
    in_path = params['infile']
    in_fld, in_fname = os.path.split(in_path)

    # Default filename is 'objects.inv'
    if not in_fname:
        in_fname = 'objects.inv'
        in_path = os.path.join(in_fld, in_fname)

    # Open the file and read
    b = readfile(in_path)
    if not b:
        print("IOError on file read attempt")
        sys.exit(1)

    # Split by newline followed by a pound sign
    l = b.split(b'\n#')

    # Most of the header is all but the last element
    h = b'\n#'.join(l[:-1])

    # The rest of the header has to be recovered from
    #  the first part of the last element
    i = b'#' + l[-1].split(b'\n')[0] + b'\n'

    # The data has to be reassembled around any incidental
    #  newlines that were present in the compressed stream
    #  before decompression by zlib
    d = zlib.decompress(
                b'\n'.join(l[-1].split(b'\n')[1:])
                        )

    # Work up the output location
    out_path = params['outfile']
    if out_path:
        out_fld, out_fname = os.path.split(out_path)
        if not out_fld:
            out_fld = in_fld
        if not out_fname:
            out_fname = os.path.splitext(in_fname)[0] + '.txt'
        out_path = os.path.join(out_fld, out_fname)
    else:
        out_fname = os.path.splitext(in_fname)[0] + '.txt'
        out_path = os.path.join(in_fld, out_fname)

    # Write the decoded file
    with open(out_path, 'wb') as f:
        f.write(h + b'\n' + i + d)

