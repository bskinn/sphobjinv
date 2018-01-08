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

ZLIB = 'zlib'
PLAIN = 'plain'
JSON_FLAT = 'json'
JSON_STRUCT = 'struct'

EXPAND = 'expand'
CONTRACT = 'contract'

CONVERT = 'convert'
SUGGEST = 'suggest'

INFILE = 'infile'
OUTFILE = 'outfile'
MODE = 'mode'
QUIET = 'quiet'

HELP_CO_PARSER = ("Convert intersphinx inventory to zlib_compressed, "
                  "plaintext, or flat and/or structured JSON.")
HELP_SU_PARSER = ("Fuzzy-search intersphinx inventory "
                  "for desired object(s).")

# MODE_NAMES = {COMP: 'compress', DECOMP: 'decompress',
#               JSON_FLAT: 'convert', JSON_STRUCT: 'convert'}

DEF_OUT_EXT = {ZLIB: '.inv', PLAIN: '.txt',
        JSON_FLAT: '.json', JSON_STRUCT: '.json'}

HELP_CONV_EXTS = "'.txt/.inv/.json'"


def _getparser():
    """Generate argument parser.

    Returns
    -------
    prs

        :class:`ArgumentParser` -- Parser for commandline usage
        of ``sphobjinv``

    """
    prs = ap.ArgumentParser(description="Format conversion for "
                                        "and introspection of "
                                        "intersphinx "
                                        "'objects.inv' files.")
    sprs = prs.add_subparsers(title='Subcommands',
                              metavar='{{{0},{1}}}'.format(CONVERT, SUGGEST),
                              help="Execution mode. Type "
                                   "'sphobjinv [mode] -h' "
                                   "for more information "
                                   "on available options. "
                                   "Mode names can be abbreviated "
                                   "to their first two letters.")
    spr_convert = sprs.add_parser(CONVERT, aliases=[CONVERT[:2]],
                                  help=HELP_CO_PARSER,
                                  description=HELP_CO_PARSER)
    spr_suggest = sprs.add_parser(SUGGEST, aliases=[SUGGEST[:2]],
                                  help=HELP_SU_PARSER,
                                  description=HELP_SU_PARSER)

    # Args for conversion subparser
    spr_convert.add_argument(MODE,
                     help="Conversion output format",
                     choices=(ZLIB, PLAIN, JSON_FLAT, JSON_STRUCT))

    spr_convert.add_argument(INFILE,
                     help="Path to file to be converted",
                     nargs=1)

    spr_convert.add_argument(OUTFILE,
                     help="Path to desired output file. "
                          "Defaults to same directory and main "
                          "file name as input file but with extension "
                          + HELP_CONV_EXTS +
                          ", as appropriate for the output format. "
                          "Bare paths are accepted here as well, "
                          "using the default output file names.",
                     nargs="?",
                     default=None)

    # Mutually exclusive group for --expand/--contract
    gp_expcont = spr_convert.add_argument_group(title="URI/display name "
                                                      "conversions")
    meg_expcont = gp_expcont.add_mutually_exclusive_group()
    meg_expcont.add_argument('-e', '--' + EXPAND,
                             help="Expand all URI and display name "
                                  "abbreviations",
                             action='store_true')

    meg_expcont.add_argument('-c', '--' + CONTRACT,
                             help="Contract all URI and display name "
                                  "abbreviations",
                             action='store_true')

    # stdout suppressor option (e.g., for scripting)
    spr_convert.add_argument('-' + QUIET[0], '--' + QUIET,
                     help="Suppress printing of status messages",
                     action='store_true')

    return prs


def resolve_inpath(in_path, mode):
    """Resolve the input file, handling mode-specific defaults."""
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

    return in_path, in_fname, in_fld


def resolve_outpath(out_path, in_fname, in_fld, mode):
    """Resolve the output file, handling mode-specific defaults."""
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

    return out_path


def import_infile(in_path):
    """Attempt import of indicated file."""
    import json

    from .inventory import Inventory as Inv

    # Try general import, for zlib or plaintext files
    try:
        inv = Inv(in_path)
    except Exception:
        pass  # Punt to JSON attempt
    else:
        return inv

    # Maybe it's JSON
    try:
        dict_json = json.load(in_path)
        inv = Inv(dict_json)
    except Exception:
        return None
    else:
        return inv


def _write_plaintext(inv, path, *, expand=False, contract=False):
    """Write plaintext from Inventory."""
    from .fileops import writefile

    b_str = inv.data_file(expand=expand, contract=contract)
    writefile(path, b_str)


def _write_zlib(inv, path, *, expand=False, contract=False):
    """Write zlib from Inventory."""
    from .fileops import writefile
    from .zlib import compress

    b_str = inv.data_file(expand=expand, contract=contract)
    bz_str = compress(b_str)
    writefile(path, bz_str)


def _write_flat_json(inv, path, *, expand=False, contract=False):
    """Write flat-dict JSON from Inventory."""
    import json

    flat_dict = inv.flat_dict(expand=expand, contract=contract)
    with open(path, 'w') as f:
        json.dump(flat_dict, f)


def _write_struct_json(inv, path, *, expand=False, contract=False):
    """Write flat-dict JSON from Inventory."""
    import json

    struct_dict = inv.struct_dict(expand=expand, contract=contract)
    with open(path, 'w') as f:
        json.dump(struct_dict, f)


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
    # directory, per default set in parser. Resolve any
    # shorthand.
    try:
        in_path, in_fname, in_fld = resolve_inpath(params[INFILE], mode)
    except Exception:
        selective_print("\nError while parsing input file path")
        sys.exit(1)

    # Attempt import
    inv = import_infile(in_path)
    if inv is None:
        selective_print("\nError: Unrecognized file format")
        sys.exit(1)

    # Work up the output location
    try:
        out_path = resolve_outpath(params[OUTFILE], in_fname, in_fld, mode)
    except Exception:
        selective_print("\nError while parsing input file path")
        sys.exit(1)

    # Write the output file
    try:
        if mode[0] == ZLIB[0]:
            _write_zlib(inv, out_path)
        if mode[0] == PLAIN[0]:
            _write_plaintext(inv, out_path)
    except Exception:
        selective_print("\nError during write of output file")
        sys.exit(1)

    # Report success, if not QUIET
    selective_print("\nConversion completed.\n"
                    "'{0}' {1}ed to '{2}'.".format(in_path, MODE_NAMES[mode],
                                                   out_path))

    # Clean exit
    sys.exit(0)


if __name__ == '__main__':    # pragma: no cover
    main()
