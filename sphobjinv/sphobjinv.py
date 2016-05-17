#-------------------------------------------------------------------------------
# Name:        sphobjinv
# Purpose:     Core module for encoding/decoding Sphinx objects.inv files
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     17 May 2016
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
import re

ENCODE = 'encode'
DECODE = 'decode'
INFILE = 'infile'
OUTFILE = 'outfile'
MODE = 'mode'

BUFSIZE = 16*1024    # 16k chunks

DEF_OUT_EXT = {ENCODE: '.inv', DECODE: '.txt'}
DEF_INP_EXT = {ENCODE: '.txt', DECODE: '.inv'}
DEF_NAME = 'objects'


# Regex pattern for comment lines
p_comments = re.compile(b'^#.*$', re.M)

# Regex pattern for not-comment lines
p_data = re.compile(b'^[^#].*$', re.M)


# Set up the argparse framework
prs = ap.ArgumentParser(description="Decode intersphinx 'objects.inv' files.")

prs.add_argument(MODE, help="Conversion mode", 
        choices=(ENCODE, DECODE))
prs.add_argument(INFILE, help="Path to 'objects.inv' type file to be decoded")
prs.add_argument(OUTFILE, help="Path to desired output file", nargs="?",
                 default=None)


def readfile(path, interactive=False):
    """ Read file contents and return as bytestring.
    """

    # Open the file and read
    try:
        with open(path, 'rb') as f:
            b = f.read()
    except Exception:
        if interactive:
            b = None
        else:
            raise

    # Return the result
    return b


def writefile(path, contents, interactive=False):
    """ Write file (with clobber) to contain the indicated contents.
    """

    # Write the decoded file
    try:
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        if interactive:
            return None
        else:
            raise

    return path


def decode(bstr):
    """ Decode an intersphinx 'objects.inv' bytestring 
    """

    # Split by newline followed by a pound sign
    pieces = bstr.split(b'\n#')

    # Most of the header is all but the last element
    hdr = b'\n#'.join(pieces[:-1])

    # The rest of the header has to be recovered from
    #  the first part of the last element
    hdr_tail = b'#' + pieces[-1].split(b'\n')[0]

    # The data has to be reassembled around any incidental
    #  newlines that were present in the compressed stream
    #  before decompression by zlib
    cdata = b'\n'.join(pieces[-1].split(b'\n')[1:])
    
    # Decompress
    data = zlib.decompress(cdata)

    # Return the newline-composited result
    return b'\n'.join([hdr, hdr_tail, data])


def encode(bstr):
    """ Encode an intersphinx 'objects.inv' bytestring
    """

    # Preconvert any DOS newlines to Unix
    s = bstr.replace(b'\r\n', b'\n')

    # Pull all of the lines
    m_comments = p_comments.findall(s)
    m_data = p_data.findall(s)

    # Assemble the binary header comments and data
    # Comments and data blocks must end in newlines
    hb = b'\n'.join(m_comments) + b'\n'
    db = b'\n'.join(m_data) + b'\n'

    # Compress the data block
    dbc = zlib.compress(db)

    # Return the composited bytestring
    return hb + dbc


def main():

    # Parse commandline arguments
    ns, args_left = prs.parse_known_args()
    params = vars(ns)

    # Conversion mode
    mode = params[MODE]

    # Infile path and name
    in_path = params[INFILE]
    in_fld, in_fname = os.path.split(in_path)

    # Default filename is 'objects.xxx'
    if not in_fname:
        in_fname = DEF_NAME + DEF_INP_EXT[mode]
        in_path = os.path.join(in_fld, in_fname)

    # Open the file and read
    bstr = readfile(in_path, True)
    if not bstr:
        print("\nError when attempting input file read")
        sys.exit(1)

    # Encode or decode per 'mode'
    if mode == DECODE:
        result = decode(bstr)
    else:
        result = encode(bstr)

    # Work up the output location
    out_path = params[OUTFILE]
    if out_path:
        out_fld, out_fname = os.path.split(out_path)
        if not out_fld:
            out_fld = in_fld
        if not out_fname:
            out_fname = os.path.splitext(in_fname)[0] + DEF_OUT_EXT[mode]
        out_path = os.path.join(out_fld, out_fname)
    else:
        out_fname = os.path.splitext(in_fname)[0] + DEF_OUT_EXT[mode]
        out_path = os.path.join(in_fld, out_fname)

    # Write the output file
    if not writefile(out_path, result, True):
        print("\nError when attempting output file write")
        sys.exit(1)

    # Report success
    print("\nConversion completed.")
    sys.exit(0)


if __name__ ==  '__main__':
    main()

