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
JSON = 'json'

EXPAND = 'expand'
CONTRACT = 'contract'

OVERWRITE = 'overwrite'

CONVERT = 'convert'
SUGGEST = 'suggest'

INFILE = 'infile'
OUTFILE = 'outfile'
MODE = 'mode'
QUIET = 'quiet'

HELP_CO_PARSER = ("Convert intersphinx inventory to zlib-compressed, "
                  "plaintext, or JSON formats.")
HELP_SU_PARSER = ("Fuzzy-search intersphinx inventory "
                  "for desired object(s).")

SUBPARSER_NAME = 'sprs_name'

DEF_OUT_EXT = {ZLIB: '.inv', PLAIN: '.txt', JSON: '.json'}

HELP_CONV_EXTS = "'.inv/.txt/.json'"


def selective_print(thing, params):
    """Print `thing` only if not `QUIET`."""
    if not params[QUIET]:
        print(thing)


def err_format(exc):
    """Pretty-format an exception."""
    return '{0}: {1}'.format(type(exc).__name__, str(exc))


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
                              dest=SUBPARSER_NAME,
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

    # ### Args for conversion subparser
    spr_convert.add_argument(MODE,
                     help="Conversion output format",
                     choices=(ZLIB, PLAIN, JSON))

    spr_convert.add_argument(INFILE,
                     help="Path to file to be converted")

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

    # Clobber argument
    spr_convert.add_argument('-' + OVERWRITE[0], '--' + OVERWRITE,
                     help="Overwrite output files without prompting",
                     action='store_true')

    # stdout suppressor option (e.g., for scripting)
    spr_convert.add_argument('-' + QUIET[0], '--' + QUIET,
                     help="Suppress printing of status messages "
                          "and overwrite output files without prompting",
                     action='store_true')

    # ### Args for suggest subparser

    return prs


def resolve_inpath(in_path):
    """Resolve the input file, handling invalid values."""
    # Path MUST be to a file
    if not os.path.isfile(in_path):
        raise FileNotFoundError('Indicated path is not a valid file')

    # Return the path as absolute
    return os.path.abspath(in_path)


def resolve_outpath(out_path, in_path, mode):
    """Resolve the output file, handling mode-specific defaults."""
    in_fld, in_fname = os.path.split(in_path)

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
        with open(in_path) as f:
            dict_json = json.load(f)
        inv = Inv(dict_json)
    except Exception:
        return None
    else:
        return inv


def write_plaintext(inv, path, *, expand=False, contract=False):
    """Write plaintext from Inventory."""
    from .fileops import writefile

    b_str = inv.data_file(expand=expand, contract=contract)
    writefile(path, b_str.replace(b'\n', os.linesep.encode('utf-8')))


def write_zlib(inv, path, *, expand=False, contract=False):
    """Write zlib from Inventory."""
    from .fileops import writefile
    from .zlib import compress

    b_str = inv.data_file(expand=expand, contract=contract)
    bz_str = compress(b_str)
    writefile(path, bz_str)


def write_json(inv, path, *, expand=False, contract=False):
    """Write JSON from Inventory."""
    import json

    if expand:
        json_dict = inv.json_dict_expanded
    elif contract:
        json_dict = inv.json_dict_contracted
    else:
        json_dict = inv.json_dict

    with open(path, 'w') as f:
        json.dump(json_dict, f)


def do_convert(inv, in_path, mode, params):
    """Carry out the conversion operation."""
    # Work up the output location
    try:
        out_path = resolve_outpath(params[OUTFILE], in_path, mode)
    except Exception as e:
        selective_print("\nError while constructing output file path:", params)
        selective_print(err_format(e), params)
        sys.exit(1)

    # If exists, confirm overwrite; clobber if QUIET
    if os.path.isfile(out_path) and not params[QUIET] and not params[OVERWRITE]:
        resp = ''
        while not (resp.lower() == 'n' or resp.lower() == 'y'):
            resp = input('File exists. Overwrite (Y/N)? ')
        if resp.lower() == 'n':
            print('\nExiting...')
            sys.exit(0)

    # Write the output file
    try:
        if mode == ZLIB:
            write_zlib(inv, out_path, expand=params[EXPAND], contract=params[CONTRACT])
        if mode == PLAIN:
            write_plaintext(inv, out_path, expand=params[EXPAND], contract=params[CONTRACT])
        if mode == JSON:
            write_json(inv, out_path, expand=params[EXPAND], contract=params[CONTRACT])
    except Exception as e:
        selective_print("\nError during write of output file:", params)
        selective_print(err_format(e), params)
        sys.exit(1)

    # Report success, if not QUIET
    selective_print("\nConversion completed.\n"
                    "'{0}' converted to '{1}' ({2}).".format(in_path,
                                                             out_path,
                                                             mode),
                    params)


def main():
    """Handle command line invocation."""
    from .fileops import readfile, writefile
    from .zlib import compress, decompress

    # Parse commandline arguments
    prs = _getparser()
    ns, args_left = prs.parse_known_args()
    params = vars(ns)

    # Conversion mode
    mode = params[MODE]

    # Resolve input file path
    try:
        in_path = resolve_inpath(params[INFILE])
    except Exception as e:
        selective_print("\nError while parsing input file path:", params)
        selective_print(err_format(e), params)
        sys.exit(1)

    # Attempt import
    inv = import_infile(in_path)
    if inv is None:
        selective_print("\nError: Unrecognized file format", params)
        sys.exit(1)

    # Perform action based upon mode
    if params[SUBPARSER_NAME][:2] == CONVERT[:2]:
        do_convert(inv, in_path, mode, params)

    # Clean exit
    sys.exit(0)


if __name__ == '__main__':    # pragma: no cover
    main()
