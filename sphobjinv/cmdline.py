# ----------------------------------------------------------------------------
# Name:        cmdline
# Purpose:     CLI module for sphobjinv
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     17 May 2016
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

"""CLI module for sphobjinv."""

import argparse as ap
import os
import sys

COMP = 'comp'
DECOMP = 'decomp'
INFILE = 'infile'
OUTFILE = 'outfile'
MODE = 'mode'
QUIET = 'quiet'

MODE_NAMES = {COMP: 'compress', DECOMP: 'decompress'}

DEF_OUT_EXT = {COMP: '.inv', DECOMP: '.txt'}
DEF_INP_EXT = {COMP: '.txt', DECOMP: '.inv'}
DEF_NAME = 'objects'

DEF_INFILE = '.'

HELP_DECOMP_EXTS = "'.txt (.inv)'"
HELP_COMP_FNAMES = "'./objects.inv(.txt)'"


def _getparser():
    """Generate argument parser.

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
                     choices=(COMP, DECOMP))

    prs.add_argument(INFILE,
                     help="Path to file to be decoded (encoded). Defaults to "
                          + HELP_COMP_FNAMES + ". "
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
                          + HELP_DECOMP_EXTS + ". "
                          "Bare paths are accepted here as well, using "
                          "the default output file names.",
                     nargs="?",
                     default=None)

    prs.add_argument('-' + QUIET[0], '--' + QUIET,
                     help="Suppress printing of status messages",
                     action='store_true')

    return prs


def main():
    """Handle command line invocation."""
    from .fileops import readfile, writefile
    from .zlib import compress, decompress

    def selective_print(thing):
        """Print `thing` only if not `QUIET`."""
        if not params[QUIET]:
            print(thing)

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
        selective_print("\nError when attempting input file read")
        sys.exit(1)

    # (De)compress per 'mode', catching and reporting
    # any raised exception
    try:
        if mode == DECOMP:
            result = decompress(bstr)
        else:
            result = compress(bstr)
    except Exception as e:
        selective_print("\nError while {0}ing '{1}':".format(MODE_NAMES[mode],
                                                             in_path))
        selective_print("\n{0}".format(repr(e)))
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
        selective_print("\nError when attempting output file write")
        sys.exit(1)

    # Report success, if not QUIET
    selective_print("\nConversion completed.\n"
                    "'{0}' {1}ed to '{2}'.".format(in_path, MODE_NAMES[mode],
                                                   out_path))

    # Clean exit
    sys.exit(0)


if __name__ == '__main__':    # pragma: no cover
    main()
