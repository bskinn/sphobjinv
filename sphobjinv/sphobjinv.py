# ----------------------------------------------------------------------------
# Name:        sphobjinv
# Purpose:     Core module for encoding/decoding Sphinx objects.inv files
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

"""Core module for sphobjinv.

Encodes/decodes objects.inv files used by intersphinx for
cross-references across different projects.

"""

import argparse as ap
import os
import zlib
import sys
import re
import io

ENCODE = 'encode'
DECODE = 'decode'
INFILE = 'infile'
OUTFILE = 'outfile'
MODE = 'mode'

BUFSIZE = 16*1024    # 16k chunks

DEF_OUT_EXT = {ENCODE: '.inv', DECODE: '.txt'}
DEF_INP_EXT = {ENCODE: '.txt', DECODE: '.inv'}
DEF_NAME = 'objects'

DEF_INFILE = '.'

HELP_DECODE_EXTS = "'.txt (.inv)'"
HELP_ENCODE_FNAMES = "'./objects.inv(.txt)'"


class SphobjinvError(Exception):
    """Exception superclass for the project."""


class VersionError(SphobjinvError):
    """Attempting an operation on an unsupported version."""


#: Bytestring regex pattern for comment lines in decoded
#: ``objects.inv`` files
p_comments = re.compile(b'^#.*$', re.M)

#: Bytestring regex pattern for data lines in decoded
#: ``objects.inv`` files
p_data = re.compile(b'^[^#].*$', re.M)


def _getparser():
    """Generate argumwnt parser.

    Returns
    -------
    prs

        :class:`ArgumentParser` -- Parser for commandline usage
        of ``sphobjinv``

    """
    prs = ap.ArgumentParser(description="Decode/encode intersphinx "
                                        "'objects.inv' files.")

    prs.add_argument(MODE,
                     help="Conversion mode",
                     choices=(ENCODE, DECODE))
    prs.add_argument(INFILE,
                     help="Path to file to be decoded (encoded). Defaults to "
                          + HELP_ENCODE_FNAMES + ". "
                          "'-' is a synonym for these defaults. "
                          "Bare paths are accepted, in which case the "
                          "preceding "
                          "default file names are used in the "
                          "indicated path.",
                     nargs="?",
                     default=DEF_INFILE)
    prs.add_argument(OUTFILE,
                     help="Path to decoded (encoded) output file. "
                          "Defaults to same directory and main "
                          "file name as input file but with extension "
                          + HELP_DECODE_EXTS + ". "
                          "Bare paths are accepted here as well, using "
                          "the default output file names.",
                     nargs="?",
                     default=None)

    return prs


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
    # Write the decoded file
    try:
        with open(path, 'wb') as f:
            f.write(contents)
    except Exception:
        if cmdline:
            return None
        else:
            raise

    return path


def decode(bstr):
    """Decode a version 2 |isphx| ``objects.inv`` bytestring.

    The `#`-prefixed comment lines are left unchanged, whereas the
    :mod:`zlib`-compressed data lines are decompressed to plaintext.

    Parameters
    ----------
    bstr

        |bytes| -- Binary string containing an encoded ``objects.inv``
        file.

    Returns
    -------
    out_b

        |bytes| -- Decoded binary string containing the plaintext
        ``objects.inv`` content.

    """
    def decompress_chunks(bstrm):
        """Handle chunk-wise zlib decompression.

        Internal function pulled from intersphinx.py@v1.4.1:
        https://github.com/sphinx-doc/sphinx/blob/1.4.1/sphinx/
          ext/intersphinx.py#L79-L124.
        BUFSIZE taken as the default value from intersphinx signature
        Modified slightly to take the stream as a parameter,
        rather than assuming one from the parent namespace.

        """
        decompressor = zlib.decompressobj()
        for chunk in iter(lambda: bstrm.read(BUFSIZE), b''):
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    # Make stream and output string
    strm = io.BytesIO(bstr)

    # Check to be sure it's v2
    out_b = strm.readline()
    if not out_b.endswith(b'2\n'):
        raise VersionError('Only v2 objects.inv files currently supported')

    # Pull name, version, and description lines
    for i in range(3):
        out_b += strm.readline()

    # Decompress chunks and append
    for chunk in decompress_chunks(strm):
        out_b += chunk

    # Replace newlines with the OS-local newlines
    out_b = out_b.replace(b'\n', os.linesep.encode())

    # Return the newline-composited result
    return out_b


def encode(bstr):
    """Encode a version 2 |isphx| ``objects.inv`` bytestring.

    The `#`-prefixed comment lines are left unchanged, whereas the
    plaintext data lines are compressed with :mod:`zlib`.

    Parameters
    ----------
    bstr

        |bytes| -- Binary string containing the decoded contents of an
        ``objects.inv`` file.

    Returns
    -------
    out_b

        |bytes| -- Binary string containing the encoded ``objects.inv``
        content.

    """
    # Preconvert any DOS newlines to Unix
    s = bstr.replace(b'\r\n', b'\n')

    # Pull all of the lines
    m_comments = p_comments.findall(s)
    m_data = p_data.finditer(s)

    # Helper generator to retrive the text, not the match object
    def gen_data():
        yield next(m_data).group(0)

    # Assemble the binary header comments and data
    # Comments and data blocks must end in newlines
    hb = b'\n'.join(m_comments) + b'\n'
    db = b'\n'.join(gen_data()) + b'\n'

    # Compress the data block
    # Compression level nine is to match that specified in
    #  sphinx html builder:
    # https://github.com/sphinx-doc/sphinx/blob/1.4.1/sphinx/
    #    builders/html.py#L843
    dbc = zlib.compress(db, 9)

    # Return the composited bytestring
    return hb + dbc


def main():
    """Handle command line invocation."""
    # Parse commandline arguments
    prs = _getparser()
    ns, args_left = prs.parse_known_args()
    params = vars(ns)

    # Conversion mode
    mode = params[MODE]

    # Infile path and name. If not specified, use current
    #  directory, per default set in parser
    in_path = params[INFILE]

    # If the input is a hyphen, replace with the default
    if in_path == "-":
        in_path = DEF_INFILE

    # If filename is actually a directory, treat as such and
    #  use the default filename. Otherwise, split accordingly
    if os.path.isdir(in_path):
        in_fld = in_path
        in_fname = None
    else:
        in_fld, in_fname = os.path.split(in_path)

    # Default filename is 'objects.xxx'
    if not in_fname:
        in_fname = DEF_NAME + DEF_INP_EXT[mode]
        in_path = os.path.join(in_fld, in_fname)

    # Open the file and read
    bstr = readfile(in_path, cmdline=True)
    if not bstr:
        print("\nError when attempting input file read")
        sys.exit(1)

    # Encode or decode per 'mode', catching and reporting
    # any raised exception
    try:
        if mode == DECODE:
            result = decode(bstr)
        else:
            result = encode(bstr)
    except Exception as e:
        print("\nError while {0}ing '{1}':".format(mode[:-1], in_path))
        print("\n{0}".format(repr(e)))
        sys.exit(1)

    # Work up the output location
    out_path = params[OUTFILE]
    if out_path:
        # Must check if the path entered is a folder
        if os.path.isdir(out_path):
            # Set just the folder and leave the name blank
            out_fld = out_path
            out_fname = None
        else:
            # Split appropriately
            out_fld, out_fname = os.path.split(out_path)

        # Output to same folder if unspecified
        if not out_fld:
            out_fld = in_fld

        # Use same base filename if not specified
        if not out_fname:
            out_fname = os.path.splitext(in_fname)[0] + DEF_OUT_EXT[mode]

        # Composite the full output path
        out_path = os.path.join(out_fld, out_fname)
    else:
        # No output location specified; use defaults
        out_fname = os.path.splitext(in_fname)[0] + DEF_OUT_EXT[mode]
        out_path = os.path.join(in_fld, out_fname)

    # Write the output file
    if not writefile(out_path, result, cmdline=True):
        print("\nError when attempting output file write")
        sys.exit(1)

    # Report success
    print("\nConversion completed.\n"
          "'{0}' {1}d to '{2}'.".format(in_path, mode, out_path))

    # Clean exit
    sys.exit(0)


if __name__ == '__main__':
    main()
