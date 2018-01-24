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

from . import __version__

# Version arg and helpers
VERSION = 'version'
VER_TXT = ("\nsphobjinv v{0}\n\n".format(__version__) +
           "Copyright (c) Brian Skinn 2016-2018\n"
           "License: The MIT License\n\n"
           "Bug reports & feature requests:"
           " https://github.com/bskinn/sphobjinv\n"
           "Documentation:"
           " {{{Add link here...}}}\n")

# Subparser selectors
CONVERT = 'convert'
SUGGEST = 'suggest'
SUBPARSER_NAME = 'sprs_name'

# Convert subparser mode var and choices
MODE = 'mode'
ZLIB = 'zlib'
PLAIN = 'plain'
JSON = 'json'

# Source/destination vars
INFILE = 'infile'
OUTFILE = 'outfile'

# Convert subparser optionals
QUIET = 'quiet'
EXPAND = 'expand'
CONTRACT = 'contract'
OVERWRITE = 'overwrite'
URL = 'url'

# Suggest subparser params
SEARCH = 'search'
THRESH = 'thresh'
INDEX = 'index'
SCORE = 'score'
ALL = 'all'

# Helper strings
HELP_CO_PARSER = ("Convert intersphinx inventory to zlib-compressed, "
                  "plaintext, or JSON formats.")
HELP_SU_PARSER = ("Fuzzy-search intersphinx inventory "
                  "for desired object(s).")

DEF_OUT_EXT = {ZLIB: '.inv', PLAIN: '.txt', JSON: '.json'}
HELP_CONV_EXTS = "'.inv/.txt/.json'"

# Suggest list length above which to prompt for confirmation
SUGGEST_CONFIRM_LENGTH = 30


def selective_print(thing, params):
    """Print `thing` only if not `QUIET`."""
    if (not params[SUBPARSER_NAME][:2] == 'co' or not params[QUIET]):
        print(thing)


def err_format(exc):
    """Pretty-format an exception."""
    return '{0}: {1}'.format(type(exc).__name__, str(exc))


def yesno_prompt(prompt):
    """Query user for yes/no confirmation."""
    resp = ''
    while not (resp.lower() == 'n' or resp.lower() == 'y'):
        resp = input(prompt)
    return resp


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
    prs.add_argument('-' + VERSION[0], '--' + VERSION,
                     help="Print package version & other info",
                     action='store_true')

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
                                  "A bare path is accepted here, "
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
                                  "and overwrite output files "
                                  "without prompting",
                             action='store_true')

    # Flag to treat infile as a URL
    spr_convert.add_argument('-' + URL[0], '--' + URL,
                             help="Treat 'infile' as a URL for download",
                             action='store_true')

    # ### Args for suggest subparser
    spr_suggest.add_argument(INFILE,
                             help="Path to inventory file to be searched")
    spr_suggest.add_argument(SEARCH,
                             help="Search term for object suggestions")
    spr_suggest.add_argument('-' + ALL[0], '--' + ALL,
                             help="Display all results "
                                  "regardless of the number returned "
                                  "without prompting for confirmation.",
                             action='store_true')
    spr_suggest.add_argument('-' + INDEX[0], '--' + INDEX,
                             help="Include Inventory.objects list indices "
                                  "with the search results",
                             action='store_true')
    spr_suggest.add_argument('-' + SCORE[0], '--' + SCORE,
                             help="Include fuzzywuzzy scores "
                                  "with the search results",
                             action='store_true')
    spr_suggest.add_argument('-' + THRESH[0], '--' + THRESH,
                             help="Match quality threshold, integer 0-100, "
                                  "default 75. Default is suitable when "
                                  "'search' is exactly a known object name. "
                                  "A value of 30-50 gives better results "
                                  "for approximate matches.",
                             default=75, type=int, choices=range(101),
                             metavar='{0-100}')
    spr_suggest.add_argument('-' + URL[0], '--' + URL,
                             help="Treat 'infile' as a URL for download",
                             action='store_true')

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
    from .fileops import readjson
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
        inv = Inv(readjson(in_path))
    except Exception:
        return None
    else:
        return inv


def write_plaintext(inv, path, *, expand=False, contract=False):
    """Write plaintext from Inventory."""
    from .fileops import writebytes

    b_str = inv.data_file(expand=expand, contract=contract)
    writebytes(path, b_str.replace(b'\n', os.linesep.encode('utf-8')))


def write_zlib(inv, path, *, expand=False, contract=False):
    """Write zlib from Inventory."""
    from .fileops import writebytes
    from .zlib import compress

    b_str = inv.data_file(expand=expand, contract=contract)
    bz_str = compress(b_str)
    writebytes(path, bz_str)


def write_json(inv, path, *, expand=False, contract=False):
    """Write JSON from Inventory."""
    from .fileops import writejson

    json_dict = inv.json_dict(expand=expand, contract=contract)
    writejson(path, json_dict)


def do_convert(inv, in_path, params):
    """Carry out the conversion operation."""
    mode = params[MODE]

    # Work up the output location
    try:
        out_path = resolve_outpath(params[OUTFILE], in_path, mode)
    except Exception as e:  # pragma: no cover
        # This may not actually be reachable except in exceptional situations
        selective_print("\nError while constructing output file path:", params)
        selective_print(err_format(e), params)
        sys.exit(1)

    # If exists, confirm overwrite; clobber if QUIET
    if (os.path.isfile(out_path) and not params[QUIET]
            and not params[OVERWRITE]):
        resp = yesno_prompt('File exists. Overwrite (Y/N)? ')
        if resp.lower() == 'n':
            print('\nExiting...')
            sys.exit(0)

    # Write the output file
    try:
        if mode == ZLIB:
            write_zlib(inv, out_path, expand=params[EXPAND],
                       contract=params[CONTRACT])
        if mode == PLAIN:
            write_plaintext(inv, out_path, expand=params[EXPAND],
                            contract=params[CONTRACT])
        if mode == JSON:
            write_json(inv, out_path, expand=params[EXPAND],
                       contract=params[CONTRACT])
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


def do_suggest(inv, params):
    """Perform the suggest call and output the results."""
    with_index = params[INDEX]
    with_score = params[SCORE]
    results = inv.suggest(params[SEARCH], thresh=params[THRESH],
                          with_index=with_index,
                          with_score=with_score)

    if len(results) == 0:
        print('\nNo results found.')
        return

    if len(results) > SUGGEST_CONFIRM_LENGTH and not params[ALL]:
        resp = yesno_prompt("Display all {0} results ".format(len(results)) +
                            "(Y/N)? ")
        if resp.lower() == 'n':
            print('\nExiting...')
            sys.exit(0)

    # Field widths in output
    SCORE_WIDTH = 7
    INDEX_WIDTH = 7

    if with_index or with_score:
        RST_WIDTH = max(len(_[0]) for _ in results)
    else:
        RST_WIDTH = max(len(_) for _ in results)

    RST_WIDTH += 2

    if with_index:
        if with_score:
            fmt = '{{0: <{0}}}  {{1: ^{1}}}  {{2: ^{2}}}'.format(RST_WIDTH,
                                                                 SCORE_WIDTH,
                                                                 INDEX_WIDTH)
            print('')
            print(fmt.format('  Name', 'Score', 'Index'))
            print(fmt.format('-' * RST_WIDTH, '-' * SCORE_WIDTH,
                             '-' * INDEX_WIDTH))
            print('\n'.join(fmt.format(*_) for _ in results))
        else:
            fmt = '{{0: <{0}}}  {{1: ^{1}}}'.format(RST_WIDTH, INDEX_WIDTH)
            print('')
            print(fmt.format('  Name', 'Index'))
            print(fmt.format('-' * RST_WIDTH, '-' * INDEX_WIDTH))
            print('\n'.join(fmt.format(*_) for _ in results))
    else:
        if with_score:
            fmt = '{{0: <{0}}}  {{1: ^{1}}}'.format(RST_WIDTH, SCORE_WIDTH)
            print('')
            print(fmt.format('  Name', 'Score'))
            print(fmt.format('-' * RST_WIDTH, '-' * SCORE_WIDTH))
            print('\n'.join(fmt.format(*_) for _ in results))
        else:
            print('\n'.join(str(_) for _ in results))


def inv_local(params):
    """Create inventory from local reference."""
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

    return inv, in_path


def inv_url(params):
    """Create inventory from downloaded URL."""
    from .inventory import Inventory

    # Disallow --url mode on local files
    if params[INFILE].startswith('file:/'):
        selective_print("\nError: URL mode on local file is invalid", params)
        sys.exit(1)

    try:
        inv = Inventory(url=params[INFILE])
    except Exception as e:
        selective_print("\nError while downloading/parsing URL:", params)
        selective_print(err_format(e), params)
        sys.exit(1)

    return inv


def main():
    """Handle command line invocation."""
    # Parse commandline arguments
    prs = _getparser()
    ns, args_left = prs.parse_known_args()
    params = vars(ns)

    # Print version &c. and exit if indicated
    if params[VERSION]:
        print(VER_TXT)
        sys.exit(0)

    # Generate the input Inventory based on --url or not
    if params[URL]:
        inv = inv_url(params)
        in_path = os.getcwd()
    else:
        inv, in_path = inv_local(params)

    # Perform action based upon mode
    if params[SUBPARSER_NAME][:2] == CONVERT[:2]:
        do_convert(inv, in_path, params)
    elif params[SUBPARSER_NAME][:2] == SUGGEST[:2]:
        do_suggest(inv, params)

    # Clean exit
    sys.exit(0)


if __name__ == '__main__':    # pragma: no cover
    main()
