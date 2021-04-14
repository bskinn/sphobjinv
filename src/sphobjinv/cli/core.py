r"""``sphobjinv`` *CLI core execution module*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    15 Nov 2020

**Copyright**
    \(c) Brian Skinn 2016-2021

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import sys

from sphobjinv.cli.load import inv_local, inv_stdin, inv_url
from sphobjinv.cli.parser import getparser, PrsConst
from sphobjinv.cli.ui import log_print, yesno_prompt
from sphobjinv.cli.write import write_file, write_stdout


def do_convert(inv, in_path, params):
    r"""Carry out the conversion operation, including writing output.

    If |cli:OVERWRITE| is passed and the output file
    (the default location, or as passed to |cli:OUTFILE|)
    exists, it will be overwritten without a prompt. Otherwise,
    the user will be queried if it is desired to overwrite
    the existing file.

    If |cli:QUIET| is passed, nothing will be
    printed to |cour|\ stdout\ |/cour|
    (potentially useful for scripting),
    and any existing output file will be overwritten
    without prompting.

    Parameters
    ----------
    inv

        |Inventory| -- Inventory object to be output in the format
        indicated by |cli:MODE|.

    in_path

        |str| -- For a local input file, its absolute path.
        For a URL, the (possibly truncated) URL text.

    params

        |dict| -- Parameters/values mapping from the active subparser

    """
    if params[PrsConst.OUTFILE] == "-" or (
        params[PrsConst.INFILE] == "-" and params[PrsConst.OUTFILE] is None
    ):
        write_stdout(inv, params)
    else:
        write_file(inv, in_path, params)


def do_suggest(inv, params):
    r"""Perform the suggest call and output the results.

    Results are printed one per line.

    If neither |cli:INDEX| nor |cli:SCORE| is specified,
    the results are output without a header.
    If either or both are specified,
    the results are output in a lightweight tabular format.

    If the number of results exceeds
    |cli:SUGGEST_CONFIRM_LENGTH|,
    the user will be queried whether to display
    all of the returned results
    unless |cli:ALL| is specified.

    No |cour|\ -\\-quiet\ |/cour| option is available here, since
    a silent mode for suggestion output is nonsensical.

    Parameters
    ----------
    inv

        |Inventory| -- Inventory object to be output in the format
        indicated by |cli:MODE|.

    params

        |dict| -- Parameters/values mapping from the active subparser

    """
    with_index = params[PrsConst.INDEX]
    with_score = params[PrsConst.SCORE]
    results = inv.suggest(
        params[PrsConst.SEARCH],
        thresh=params[PrsConst.THRESH],
        with_index=with_index,
        with_score=with_score,
    )

    if len(results) == 0:
        log_print("No results found.", params)
        return

    # Query if the results are long enough, but not if '--all' has been
    # passed or if the data is coming via stdin (reading from stdin breaks
    # the terminal interactions)
    if (
        len(results) > PrsConst.SUGGEST_CONFIRM_LENGTH
        and not params[PrsConst.ALL]
        and params[PrsConst.INFILE] != "-"
    ):
        resp = yesno_prompt(f"Display all {len(results)} results (Y/N)?")
        if resp.lower() == "n":
            log_print("\nExiting...", params)
            sys.exit(0)

    # Field widths in output
    score_width = 7
    index_width = 7

    if with_index or with_score:
        rst_width = max(len(res[0]) for res in results)
    else:
        rst_width = max(len(res) for res in results)

    rst_width += 2

    if with_index:
        if with_score:
            fmt = f"{{0: <{rst_width}}}  {{1: ^{score_width}}}  {{2: ^{index_width}}}"
            print(fmt.format("  Name", "Score", "Index"))
            print(fmt.format("-" * rst_width, "-" * score_width, "-" * index_width))
            print("\n".join(fmt.format(*_) for _ in results))
        else:
            fmt = f"{{0: <{rst_width}}}  {{1: ^{index_width}}}"
            print(fmt.format("  Name", "Index"))
            print(fmt.format("-" * rst_width, "-" * index_width))
            print("\n".join(fmt.format(*_) for _ in results))
    else:
        if with_score:
            fmt = f"{{0: <{rst_width}}}  {{1: ^{score_width}}}"
            print(fmt.format("  Name", "Score"))
            print(fmt.format("-" * rst_width, "-" * score_width))
            print("\n".join(fmt.format(*_) for _ in results))
        else:
            print("\n".join(str(_) for _ in results))


def main():
    r"""Handle command line invocation.

    Parses command line arguments,
    handling the no-arguments and
    |cli:VERSION| cases.

    Creates the |Inventory| from the indicated source
    and method.

    Invokes :func:`do_convert` or :func:`do_suggest`
    per the subparser name stored in |cli:SUBPARSER_NAME|.

    """
    # If no args passed, stick in '-h'
    if len(sys.argv) == 1:
        sys.argv.append("-h")

    # Parse commandline arguments
    prs = getparser()
    ns, args_left = prs.parse_known_args()
    params = vars(ns)

    # Print version &c. and exit if indicated
    if params[PrsConst.VERSION]:
        print(PrsConst.VER_TXT)
        sys.exit(0)

    # Regardless of mode, insert extra blank line
    # for cosmetics
    log_print(" ", params)

    # Generate the input Inventory based on --url or stdio or file.
    # These inventory-load functions should call
    # sys.exit(n) internally in error-exit situations
    if params[PrsConst.URL]:
        if params[PrsConst.INFILE] == "-":
            prs.error("argument -u/--url not allowed with '-' as infile")
        inv, in_path = inv_url(params)
    elif params[PrsConst.INFILE] == "-":
        inv = inv_stdin(params)
        in_path = None
    else:
        inv, in_path = inv_local(params)

    # Perform action based upon mode
    if params[PrsConst.SUBPARSER_NAME][:2] == PrsConst.CONVERT[:2]:
        do_convert(inv, in_path, params)
    elif params[PrsConst.SUBPARSER_NAME][:2] == PrsConst.SUGGEST[:2]:
        do_suggest(inv, params)

    # Cosmetic final blank line
    log_print(" ", params)

    # Clean exit
    sys.exit(0)
