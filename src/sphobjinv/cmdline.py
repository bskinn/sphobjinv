r"""*CLI module for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

.. note::

    This module is NOT part of the public API for ``sphobjinv``.
    Its entire contents should be considered implementation detail.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    17 May 2016

**Copyright**
    \(c) Brian Skinn 2016-2020

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import argparse as ap
import json
import os
import sys
from json.decoder import JSONDecodeError
from urllib.error import HTTPError, URLError

from jsonschema.exceptions import ValidationError

from sphobjinv import __version__
from sphobjinv.error import VersionError
from sphobjinv.fileops import readjson, urlwalk, writebytes, writejson
from sphobjinv.inventory import Inventory as Inv
from sphobjinv.zlib import compress


# ### Version arg and helpers
#: Optional argument name for use with the base
#: argument parser, to show version &c. info, and exit
VERSION = "version"

#: Version &c. output blurb
VER_TXT = (
    "\nsphobjinv v{0}\n\n".format(__version__) + "Copyright (c) Brian Skinn 2016-2020\n"
    "License: The MIT License\n\n"
    "Bug reports & feature requests:"
    " https://github.com/bskinn/sphobjinv\n"
    "Documentation:"
    " https://sphobjinv.readthedocs.io\n"
)

# ### Subparser selectors and argparse param for storing subparser name
#: Subparser name for inventory file conversions; stored in
#: :data:`SUBPARSER_NAME` when selected
CONVERT = "convert"

#: Subparser name for inventory object suggestions; stored in
#: :data:`SUBPARSER_NAME` when selected
SUGGEST = "suggest"

#: Param for storing subparser name
#: (:data:`CONVERT` or :data:`SUGGEST`)
SUBPARSER_NAME = "sprs_name"

# ### Common URL argument for both subparsers
#: Optional argument name for use with both :data:`CONVERT` and
#: :data:`SUGGEST` subparsers, indicating that
#: :data:`INFILE` is to be treated as a URL
#: rather than a local file path
URL = "url"

# ### Conversion subparser: 'mode' param and choices
#: Positional argument name for use with :data:`CONVERT` subparser,
#: indicating output file format
#: (:data:`ZLIB`, :data:`PLAIN` or :data:`JSON`)
MODE = "mode"

#: Argument value for :data:`CONVERT` :data:`MODE`,
#: to output a :mod:`zlib`-compressed inventory
ZLIB = "zlib"

#: Argument value for :data:`CONVERT` :data:`MODE`,
#: to output a plaintext inventory
PLAIN = "plain"

#: Argument value for :data:`CONVERT` :data:`MODE`,
#: to output an inventory as JSON
JSON = "json"

# ### Source/destination params
#: Required positional argument name for use with both :data:`CONVERT` and
#: :data:`SUGGEST` subparsers, holding the path
#: (or URL, if :data:`URL` is specified)
#: to the input file
INFILE = "infile"

#: Optional positional argument name
#: for use with the :data:`CONVERT` subparser,
#: holding the path to the output file
#: (:data:`DEF_BASENAME` and the appropriate item from :data:`DEF_OUT_EXT`
#: are used if this argument is not provided)
OUTFILE = "outfile"

# ### Convert subparser optional params
#: Optional argument name for use with the :data:`CONVERT` subparser,
#: indicating to suppress console output
QUIET = "quiet"

#: Optional argument name for use with the :data:`CONVERT` subparser,
#: indicating to expand URI and display name
#: abbreviations in the generated output file
EXPAND = "expand"

#: Optional argument name for use with the :data:`CONVERT` subparser,
#: indicating to contract URIs and display names
#: to abbreviated forms in the generated output file
CONTRACT = "contract"

#: Optional argument name for use with the :data:`CONVERT` subparser,
#: indicating to overwrite any existing output
#: file without prompting
OVERWRITE = "overwrite"

# ### Suggest subparser params
#: Positional argument name for use with the :data:`SUGGEST` subparser,
#: holding the search term for |fuzzywuzzy|_ text matching
SEARCH = "search"

#: Optional argument name for use with the :data:`SUGGEST` subparser,
#: taking the minimum desired |fuzzywuzzy|_ match quality
#: as one required argument
THRESH = "thresh"

#: Optional argument name for use with the :data:`SUGGEST` subparser,
#: indicating to print the location index of each returned object
#: within :data:`INFILE` along with the object domain/role/name
#: (may be specified with :data:`SCORE`)
INDEX = "index"

#: Optional argument name for use with the :data:`SUGGEST` subparser,
#: indicating to print the |fuzzywuzzy|_ score of each returned object
#: within :data:`INFILE` along with the object domain/role/name
#: (may be specified with :data:`INDEX`)
SCORE = "score"

#: Optional argument name for use with the :data:`SUGGEST` subparser,
#: indicating to print all returned objects, regardless of the
#: number returned, without asking for confirmation
ALL = "all"

# ### Helper strings
#: Help text for the :data:`CONVERT` subparser
HELP_CO_PARSER = (
    "Convert intersphinx inventory to zlib-compressed, plaintext, or JSON formats."
)

#: Help text for the :data:`SUGGEST` subparser
HELP_SU_PARSER = "Fuzzy-search intersphinx inventory for desired object(s)."

#: Help text for default extensions for the various conversion types
HELP_CONV_EXTS = "'.inv/.txt/.json'"

# ### Defaults for an unspecified OUTFILE
#: Default base name for an unspecified :data:`OUTFILE`
DEF_BASENAME = "objects"

#: Default extensions for an unspecified :data:`OUTFILE`
DEF_OUT_EXT = {ZLIB: ".inv", PLAIN: ".txt", JSON: ".json"}

# ### Useful constants
#: Number of returned objects from a :data:`SUGGEST` subparser invocation
#: above which user will be prompted for confirmation to print the results
#: (unless :data:`ALL` is specified)
SUGGEST_CONFIRM_LENGTH = 30

#: Default match threshold for :option:`sphobjinv suggest --thresh`
DEF_THRESH = 75

#: Dict key for URL at which an inventory was actually found
FOUND_URL = "found_url"


def log_print(thing, params):
    """Print `thing` to stderr if not in quiet mode.

    Quiet mode is indicated by the value at the :data:`QUIET` key
    within `params`.

    Quiet mode is not implemented for the ":doc:`suggest </cli/suggest>`"
    CLI mode.

    Parameters
    ----------
    thing

        *any* -- Object to be printed

    params

        |dict| -- Parameters/values mapping from the active subparser

    """
    if not params[SUBPARSER_NAME][:2] == "co" or not params[QUIET]:
        print(thing, file=sys.stderr)


def err_format(exc):
    r"""Pretty-format an exception.

    Parameters
    ----------
    exc

        :class:`Exception` -- Exception instance to pretty-format

    Returns
    -------
    pretty_exc

        |str| -- Exception type and message formatted as
        |cour|\ '{type}: {message}'\ |/cour|

    """
    return "{0}: {1}".format(type(exc).__name__, str(exc))


def yesno_prompt(prompt):
    r"""Query user at `stdin` for yes/no confirmation.

    Uses :func:`input`, so will hang if used programmatically
    unless `stdin` is suitably mocked.

    The value returned from :func:`input` must satisfy either
    |cour|\ resp.lower() == 'n'\ |/cour| or
    |cour|\ resp.lower() == 'y'\ |/cour|,
    or else the query will be repeated *ad infinitum*.
    This function does **NOT** augment `prompt`
    to indicate the constraints on the accepted values.

    Parameters
    ----------
    prompt

        |str| -- Prompt to display to user that
        requests a 'Y' or 'N' response

    Returns
    -------
    resp

        |str| -- User response

    """
    resp = ""
    while not (resp.lower() == "n" or resp.lower() == "y"):
        resp = input(prompt)  # noqa: S322
    return resp


def getparser():
    """Generate argument parser.

    Returns
    -------
    prs

        :class:`~argparse.ArgumentParser` -- Parser for commandline usage
        of ``sphobjinv``

    """
    prs = ap.ArgumentParser(
        description="Format conversion for "
        "and introspection of "
        "intersphinx "
        "'objects.inv' files."
    )
    prs.add_argument(
        "-" + VERSION[0],
        "--" + VERSION,
        help="Print package version & other info",
        action="store_true",
    )

    sprs = prs.add_subparsers(
        title="Subcommands",
        dest=SUBPARSER_NAME,
        metavar="{{{0},{1}}}".format(CONVERT, SUGGEST),
        help="Execution mode. Type "
        "'sphobjinv [mode] -h' "
        "for more information "
        "on available options. "
        "Mode names can be abbreviated "
        "to their first two letters.",
    )

    # Enforce subparser as optional. No effect for 3.4 to 3.7;
    # briefly required a/o 3.7.0b4 due to change in default behavior, per:
    # https://bugs.python.org/issue33109. 3.6 behavior restored for
    # 3.7 release.
    sprs.required = False

    spr_convert = sprs.add_parser(
        CONVERT, aliases=[CONVERT[:2]], help=HELP_CO_PARSER, description=HELP_CO_PARSER
    )
    spr_suggest = sprs.add_parser(
        SUGGEST, aliases=[SUGGEST[:2]], help=HELP_SU_PARSER, description=HELP_SU_PARSER
    )

    # ### Args for conversion subparser
    spr_convert.add_argument(
        MODE, help="Conversion output format", choices=(ZLIB, PLAIN, JSON)
    )

    spr_convert.add_argument(
        INFILE,
        help=(
            "Path to file to be converted. Passing '-' indicates to read from stdin "
            "(plaintext/JSON only)."
        ),
    )

    spr_convert.add_argument(
        OUTFILE,
        help=(
            "Path to desired output file. "
            "Defaults to same directory and main "
            "file name as input file but with extension "
            + HELP_CONV_EXTS
            + ", as appropriate for the output format. "
            "A path to a directory is accepted here, "
            "in which case the default output file name will be used. "
            "Passing '-' indicates to write to stdout. If "
            + INFILE
            + " is passed as '-', "
            + OUTFILE
            + " can be omitted and both stdin and stdout will be used."
        ),
        nargs="?",
        default=None,
    )

    # Mutually exclusive group for --expand/--contract
    gp_expcont = spr_convert.add_argument_group(title="URI/display name conversions")
    meg_expcont = gp_expcont.add_mutually_exclusive_group()
    meg_expcont.add_argument(
        "-e",
        "--" + EXPAND,
        help="Expand all URI and display name abbreviations",
        action="store_true",
    )

    meg_expcont.add_argument(
        "-c",
        "--" + CONTRACT,
        help="Contract all URI and display name abbreviations",
        action="store_true",
    )

    # Clobber argument
    spr_convert.add_argument(
        "-" + OVERWRITE[0],
        "--" + OVERWRITE,
        help="Overwrite output files without prompting",
        action="store_true",
    )

    # stdout suppressor option (e.g., for scripting)
    spr_convert.add_argument(
        "-" + QUIET[0],
        "--" + QUIET,
        help="Suppress printing of status messages "
        "and overwrite output files "
        "without prompting",
        action="store_true",
    )

    # Flag to treat infile as a URL
    spr_convert.add_argument(
        "-" + URL[0],
        "--" + URL,
        help="Treat 'infile' as a URL for download",
        action="store_true",
    )

    # ### Args for suggest subparser
    spr_suggest.add_argument(
        INFILE,
        help=(
            "Path to inventory file to be searched. "
            "Passing '-' indicates to read from stdin (plaintext/JSON only)."
        ),
    )
    spr_suggest.add_argument(SEARCH, help="Search term for object suggestions")
    spr_suggest.add_argument(
        "-" + ALL[0],
        "--" + ALL,
        help="Display all results "
        "regardless of the number returned "
        "without prompting for confirmation.",
        action="store_true",
    )
    spr_suggest.add_argument(
        "-" + INDEX[0],
        "--" + INDEX,
        help="Include Inventory.objects list indices with the search results",
        action="store_true",
    )
    spr_suggest.add_argument(
        "-" + SCORE[0],
        "--" + SCORE,
        help="Include fuzzywuzzy scores with the search results",
        action="store_true",
    )
    spr_suggest.add_argument(
        "-" + THRESH[0],
        "--" + THRESH,
        help="Match quality threshold, integer 0-100, "
        "default 75. Default is suitable when "
        "'search' is exactly a known object name. "
        "A value of 30-50 gives better results "
        "for approximate matches.",
        default=DEF_THRESH,
        type=int,
        choices=range(101),
        metavar="{0-100}",
    )
    spr_suggest.add_argument(
        "-" + URL[0],
        "--" + URL,
        help="Treat 'infile' as a URL for download",
        action="store_true",
    )

    return prs


def resolve_inpath(in_path):
    """Resolve the input file, handling invalid values.

    Currently, only checks for existence and not-directory.

    Parameters
    ----------
    in_path

        |str| -- Path to desired input file

    Returns
    -------
    abs_path

        |str| -- Absolute path to indicated file

    Raises
    ------
    :exc:`FileNotFoundError`

        If a file is not found at the given path

    """
    # Path MUST be to a file, that exists
    if not os.path.isfile(in_path):
        raise FileNotFoundError("Indicated path is not a valid file")

    # Return the path as absolute
    return os.path.abspath(in_path)


def resolve_outpath(out_path, in_path, params):
    r"""Resolve the output location, handling mode-specific defaults.

    If the output path or basename are not specified, they are
    taken as the same as the input file. If the extension is
    unspecified, it is taken as the appropriate mode-specific value
    from :data:`DEF_OUT_EXT`.

    If :data:`URL` is passed, the input directory
    is taken to be :func:`os.getcwd` and the input basename
    is taken as :data:`DEF_BASENAME`.

    Parameters
    ----------
    out_path

        |str| or |None| -- Output location provided by the user,
        or |None| if omitted

    in_path

        |str| -- For a local input file, its absolute path.
        For a URL, the (possibly truncated) URL text.

    params

        |dict| -- Parameters/values mapping from the active subparser

    Returns
    -------
    out_path

        |str| -- Absolute path to the target output file

    """
    mode = params[MODE]

    if params[URL] or in_path is None:
        in_fld = os.getcwd()
        in_fname = DEF_BASENAME
    else:
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
    """Attempt import of indicated file.

    Convenience function wrapping attempts to load an
    |Inventory| from a local path.

    Parameters
    ----------
    in_path

        |str| -- Path to input file

    Returns
    -------
    inv

        |Inventory| or |None| -- If instantiation with the file at
        `in_path` succeeds, the resulting |Inventory| instance;
        otherwise, |None|

    """
    # Try general import, for zlib or plaintext files
    try:
        inv = Inv(in_path)
    except AttributeError:
        pass  # Punt to JSON attempt
    else:
        return inv

    # Maybe it's JSON
    try:
        inv = Inv(readjson(in_path))
    except JSONDecodeError:
        return None
    else:
        return inv


def write_plaintext(inv, path, *, expand=False, contract=False):
    """Write an |Inventory| to plaintext.

    Newlines are inserted in an OS-aware manner,
    based on the value of :data:`os.linesep`.

    Calling with both `expand` and `contract` as |True| is invalid.

    Parameters
    ----------
    inv

        |Inventory| -- Objects inventory to be written as plaintext

    path

        |str| -- Path to output file

    expand

        |bool| *(optional)* -- Generate output with any
        :data:`~sphobjinv.data.SuperDataObj.uri` or
        :data:`~sphobjinv.data.SuperDataObj.dispname`
        abbreviations expanded

    contract

        |bool| *(optional)* -- Generate output with abbreviated
        :data:`~sphobjinv.data.SuperDataObj.uri` and
        :data:`~sphobjinv.data.SuperDataObj.dispname` values

    Raises
    ------
    ValueError

        If both `expand` and `contract` are |True|

    """
    b_str = inv.data_file(expand=expand, contract=contract)
    writebytes(path, b_str.replace(b"\n", os.linesep.encode("utf-8")))


def write_zlib(inv, path, *, expand=False, contract=False):
    """Write an |Inventory| to zlib-compressed format.

       Calling with both `expand` and `contract` as |True| is invalid.

    Parameters
    ----------
    inv

        |Inventory| -- Objects inventory to be written zlib-compressed

    path

        |str| -- Path to output file

    expand

        |bool| *(optional)* -- Generate output with any
        :data:`~sphobjinv.data.SuperDataObj.uri` or
        :data:`~sphobjinv.data.SuperDataObj.dispname`
        abbreviations expanded

    contract

        |bool| *(optional)* -- Generate output with abbreviated
        :data:`~sphobjinv.data.SuperDataObj.uri` and
        :data:`~sphobjinv.data.SuperDataObj.dispname` values

    Raises
    ------
    ValueError

        If both `expand` and `contract` are |True|

    """
    b_str = inv.data_file(expand=expand, contract=contract)
    bz_str = compress(b_str)
    writebytes(path, bz_str)


def write_json(inv, path, params):
    """Write an |Inventory| to JSON.

    Writes output via
    :func:`fileops.writejson() <sphobjinv.fileops.writejson>`.

    Calling with both `expand` and `contract` as |True| is invalid.

    Parameters
    ----------
    inv

        |Inventory| -- Objects inventory to be written zlib-compressed

    path

        |str| -- Path to output file

    params

        dict -- `argparse` parameters

    Raises
    ------
    ValueError

        If both `params["expand"]` and `params["contract"]` are |True|

    """
    json_dict = inv.json_dict(expand=params[EXPAND], contract=params[CONTRACT])

    if params.get(FOUND_URL, False):
        json_dict.update({"metadata": {URL: params[FOUND_URL]}})

    writejson(path, json_dict)


def write_stdout(inv, params):
    r"""Write the inventory contents to stdout.

    Parameters
    ----------
    inv

        |Inventory| -- Objects inventory to be written to stdout

    params

        dict -- `argparse` parameters

    Raises
    ------
    ValueError

        If both `params["expand"]` and `params["contract"]` are |True|

    """
    if params[MODE] == PLAIN:
        print(inv.data_file(expand=params[EXPAND], contract=params[CONTRACT]).decode())
    elif params[MODE] == JSON:
        json_dict = inv.json_dict(expand=params[EXPAND], contract=params[CONTRACT])

        if params.get(FOUND_URL, False):
            json_dict.update({"metadata": {URL: params[FOUND_URL]}})

        print(json.dumps(json_dict))
    else:
        log_print("Error: Only plaintext and JSON can be emitted to stdout.", params)
        sys.exit(1)


def do_convert(inv, in_path, params):
    r"""Carry out the conversion operation, including writing output.

    If :data:`OVERWRITE` is passed and the output file
    (the default location, or as passed to :data:`OUTFILE`)
    exists, it will be overwritten without a prompt. Otherwise,
    the user will be queried if it is desired to overwrite
    the existing file.

    If :data:`QUIET` is passed, nothing will be
    printed to |cour|\ stdout\ |/cour|
    (potentially useful for scripting),
    and any existing output file will be overwritten
    without prompting.

    Parameters
    ----------
    inv

        |Inventory| -- Inventory object to be output in the format
        indicated by :data:`MODE`.

    in_path

        |str| -- For a local input file, its absolute path.
        For a URL, the (possibly truncated) URL text.

    params

        |dict| -- Parameters/values mapping from the active subparser

    """
    # TODO: Refactor to-file output to new function
    # TODO: Add tests for stdout output functionality
    if params[OUTFILE] == "-" or (params[INFILE] == "-" and params[OUTFILE] is None):
        write_stdout(inv, params)
        return

    mode = params[MODE]

    # Work up the output location
    try:
        out_path = resolve_outpath(params[OUTFILE], in_path, params)
    except Exception as e:  # pragma: no cover
        # This may not actually be reachable except in exceptional situations
        log_print("\nError while constructing output file path:", params)
        log_print(err_format(e), params)
        sys.exit(1)

    # If exists, confirm overwrite; clobber if QUIET
    if os.path.isfile(out_path) and not params[QUIET] and not params[OVERWRITE]:
        resp = yesno_prompt("File exists. Overwrite (Y/N)? ")
        if resp.lower() == "n":
            log_print("\nExiting...", params)
            sys.exit(0)

    # Write the output file
    try:
        if mode == ZLIB:
            write_zlib(inv, out_path, expand=params[EXPAND], contract=params[CONTRACT])
        if mode == PLAIN:
            write_plaintext(
                inv, out_path, expand=params[EXPAND], contract=params[CONTRACT]
            )
        if mode == JSON:
            write_json(inv, out_path, params)
    except Exception as e:
        log_print("\nError during write of output file:", params)
        log_print(err_format(e), params)
        sys.exit(1)

    # Report success, if not QUIET
    log_print(
        "Conversion completed.\n"
        "'{0}' converted to '{1}' ({2}).".format(
            in_path if in_path else "stdin", out_path, mode
        ),
        params,
    )


def do_suggest(inv, params):
    r"""Perform the suggest call and output the results.

    Results are printed one per line.

    If neither :data:`INDEX` nor :data:`SCORE` is specified,
    the results are output without a header.
    If either or both are specified,
    the results are output in a lightweight tabular format.

    If the number of results exceeds
    :data:`SUGGEST_CONFIRM_LENGTH`,
    the user will be queried whether to display
    all of the returned results
    unless :data:`ALL` is specified.

    No |cour|\ -\\-quiet\ |/cour| option is available here, since
    a silent mode for suggestion output is nonsensical.

    Parameters
    ----------
    inv

        |Inventory| -- Inventory object to be output in the format
        indicated by :data:`MODE`.

    params

        |dict| -- Parameters/values mapping from the active subparser

    """
    with_index = params[INDEX]
    with_score = params[SCORE]
    results = inv.suggest(
        params[SEARCH],
        thresh=params[THRESH],
        with_index=with_index,
        with_score=with_score,
    )

    if len(results) == 0:
        log_print("No results found.", params)
        return

    if len(results) > SUGGEST_CONFIRM_LENGTH and not params[ALL]:
        resp = yesno_prompt("Display all {0} results (Y/N)?".format(len(results)))
        if resp.lower() == "n":
            log_print("\nExiting...", params)
            sys.exit(0)

    # Field widths in output
    score_width = 7
    index_width = 7

    if with_index or with_score:
        rst_width = max(len(_[0]) for _ in results)
    else:
        rst_width = max(len(_) for _ in results)

    rst_width += 2

    if with_index:
        if with_score:
            fmt = "{{0: <{0}}}  {{1: ^{1}}}  {{2: ^{2}}}".format(
                rst_width, score_width, index_width
            )
            print("")
            print(fmt.format("  Name", "Score", "Index"))
            print(fmt.format("-" * rst_width, "-" * score_width, "-" * index_width))
            print("\n".join(fmt.format(*_) for _ in results))
        else:
            fmt = "{{0: <{0}}}  {{1: ^{1}}}".format(rst_width, index_width)
            print("")
            print(fmt.format("  Name", "Index"))
            print(fmt.format("-" * rst_width, "-" * index_width))
            print("\n".join(fmt.format(*_) for _ in results))
    else:
        if with_score:
            fmt = "{{0: <{0}}}  {{1: ^{1}}}".format(rst_width, score_width)
            print("")
            print(fmt.format("  Name", "Score"))
            print(fmt.format("-" * rst_width, "-" * score_width))
            print("\n".join(fmt.format(*_) for _ in results))
        else:
            print("\n".join(str(_) for _ in results))


def inv_local(params):
    """Create |Inventory| from local source.

    Uses :func:`resolve_inpath` to sanity-check and/or convert
    :data:`INFILE`.

    Calls :func:`sys.exit` internally in error-exit situations.

    Parameters
    ----------
    params

        |dict| -- Parameters/values mapping from the active subparser

    Returns
    -------
    inv

        |Inventory| -- Object representation of the inventory
        at :data:`INFILE`

    in_path

        |str| -- Input file path as resolved/checked by
        :func:`resolve_inpath`

    """
    # Resolve input file path
    try:
        in_path = resolve_inpath(params[INFILE])
    except Exception as e:
        log_print("\nError while parsing input file path:", params)
        log_print(err_format(e), params)
        sys.exit(1)

    # Attempt import
    inv = import_infile(in_path)
    if inv is None:
        log_print("\nError: Unrecognized file format", params)
        sys.exit(1)

    return inv, in_path


def inv_url(params):
    """Create |Inventory| from file downloaded from URL.

    Initially, treats :data:`INFILE` as a download URL to be passed to
    the `url` initialization argument
    of :class:`~sphobjinv.inventory.Inventory`.

    If an inventory is not found at that exact URL, progressively
    searches the directory tree of the URL for |objects.inv|.

    Injects the URL at which an inventory was found into `params`
    under the :data:`FOUND_URL` key.

    Calls :func:`sys.exit` internally in error-exit situations.

    Parameters
    ----------
    params

        |dict| -- Parameters/values mapping from the active subparser

    Returns
    -------
    inv

        |Inventory| -- Object representation of the inventory
        at :data:`INFILE`

    ret_path

        |str| -- URL from :data:`INFILE` used to construct `inv`.
        If URL is longer than 45 characters, the central portion is elided.

    """
    in_file = params[INFILE]

    # Disallow --url mode on local files
    if in_file.startswith("file:/"):
        log_print("\nError: URL mode on local file is invalid", params)
        sys.exit(1)

    # Need to initialize the inventory variable
    inv = None

    # Try URL as provided
    try:
        inv = Inv(url=in_file)
    except (HTTPError, ValueError, VersionError, URLError):
        log_print("No inventory at provided URL.", params)
    else:
        log_print("Remote inventory found.", params)
        url = in_file

    # Keep searching if inv not found yet
    if not inv:
        for url in urlwalk(in_file):
            log_print('Attempting "{0}" ...'.format(url), params)
            try:
                inv = Inv(url=url)
            except (ValueError, HTTPError):
                pass
            else:
                log_print("Remote inventory found.", params)
                break

    # Cosmetic line break
    log_print(" ", params)

    # Success or no?
    if not inv:
        log_print("No inventory found!", params)
        sys.exit(1)

    params.update({FOUND_URL: url})
    if len(url) > 45:
        ret_path = url[:20] + "[...]" + url[-20:]
    else:  # pragma: no cover
        ret_path = url

    return inv, ret_path


def inv_stdin(params):
    """Create |Inventory| from contents of stdin.

    Due to stdin's encoding and formatting assumptions, only
    text-based inventory formats can be sanely parsed.

    Thus, only plaintext and JSON inventory formats can be
    used as inputs here

    Parameters
    ----------
    params

        |dict| -- Parameters/values mapping from the active subparser

    Returns
    -------
    inv

        |Inventory| -- Object representation of the inventory
        provided at stdin

    """
    data = sys.stdin.read()

    try:
        return Inv(dict_json=json.loads(data))
    except (JSONDecodeError, ValidationError):
        pass

    try:
        return Inv(plaintext=data)
    except (AttributeError, UnicodeEncodeError, TypeError):
        pass

    log_print("Invalid plaintext or JSON inventory format.", params)
    sys.exit(1)


def main():
    r"""Handle command line invocation.

    Parses command line arguments,
    handling the no-arguments and
    :data:`VERSION` cases.

    Creates the |Inventory| from the indicated source
    and method.

    Invokes :func:`do_convert` or :func:`do_suggest`
    per the subparser name stored in :data:`SUBPARSER_NAME`.

    """
    # If no args passed, stick in '-h'
    if len(sys.argv) == 1:
        sys.argv.append("-h")

    # Parse commandline arguments
    prs = getparser()
    ns, args_left = prs.parse_known_args()
    params = vars(ns)

    # TODO: Per #131, force quiet mode if converting to stdout

    # Print version &c. and exit if indicated
    if params[VERSION]:
        print(VER_TXT)
        sys.exit(0)

    # Regardless of mode, insert extra blank line
    # for cosmetics
    log_print(" ", params)

    # Generate the input Inventory based on --url or stdio or file.
    # These inventory-load functions should call
    # sys.exit(n) internally in error-exit situations
    if params[URL]:
        inv, in_path = inv_url(params)
    elif params[INFILE] == "-":
        # TODO: Add tests for stdin-read functionality
        inv = inv_stdin(params)
        in_path = None
    else:
        inv, in_path = inv_local(params)

    # Perform action based upon mode
    if params[SUBPARSER_NAME][:2] == CONVERT[:2]:
        do_convert(inv, in_path, params)
    elif params[SUBPARSER_NAME][:2] == SUGGEST[:2]:
        do_suggest(inv, params)

    # Cosmetic final blank line
    log_print(" ", params)

    # Clean exit
    sys.exit(0)
