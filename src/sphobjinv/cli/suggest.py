r"""``sphobjinv`` *module for CLI suggest functionality*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    20 Oct 2022

**Copyright**
    \(c) Brian Skinn 2016-2022

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import sys

from sphobjinv.cli.parser import PrsConst
from sphobjinv.cli.ui import print_stderr, yesno_prompt


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

    No |cli:QUIET| option is available here, since
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

    print_stderr(f"{inv.count} objects in inventory.\n", params)

    log_print_result_count(params, results)

    # TODO: Print inferred intersphinx_mapping
    #  - If input URL is the objinv URL and objinv base finder is a no-op,
    #    then can't infer mapping
    #  - If input URL is the objinv URL and objinv base finder IS NOT a no-op,
    #    then mapping inferred from objinv base finder and None is PROBABLY
    #    reliable.
    #  - If input URL is NOT the objinv URL and objinv base finder is a no-op,
    #    then SOMETHING WEIRD HAPPENED.
    #  - If input URL is NOT the objinv URL and objinv base find IS NOT a no-op,
    #    then mapping inferred from objinv base finder and None is STRONGLY
    #    reliable.

    # The confirmation query here is conditional; see the function docstring.
    confirm_print_if_long_list(params, results)

    log_print_results_table(with_index, with_score, results)


def log_print_result_count(params, results):
    """Report the count of found objects from the suggest search."""
    if len(results) == 0:
        print_stderr(
            (
                "No results found with score at/above current threshold of "
                f"{params[PrsConst.THRESH]}."
            ),
            params,
        )
        sys.exit(0)
    else:
        print_stderr(
            (
                f"{len(results)} result"
                f"{'' if len(results) == 1 else 's'}"
                " found at/above current threshold of "
                f"{params[PrsConst.THRESH]}.\n"
            ),
            params,
        )


def confirm_print_if_long_list(params, results):
    """Check if the results list is too long and query user if to proceed.

    Skip the check if ``--all`` has been passed.

    Also skip the check if receiving data from ``stdin``, as a stream
    interaction here fouls the data flow...I forget exactly how.

    """

    if (
        len(results) > PrsConst.SUGGEST_CONFIRM_LENGTH
        and not params[PrsConst.ALL]
        and params[PrsConst.INFILE] != "-"
    ):
        resp = yesno_prompt(f"Display all {len(results)} results (Y/N)?")
        if resp.lower() == "n":
            print_stderr("\nExiting...", params)
            sys.exit(0)


def log_print_results_table(with_index, with_score, results):
    """Prepare and print the table of suggest search results."""
    # Field widths in output
    score_width = 7
    index_width = 7

    # This is necessary because the results are returned as a
    # list[str] if neither index nor score is included; but are
    # returned as a list[tuple[...]] if one or both of index/score
    # is included.
    if with_index or with_score:
        rst_width = max(len(res[0]) for res in results)
    else:
        rst_width = max(len(res) for res in results)

    rst_width += 2

    # For now, in each case the formatting for each row is dynamically
    # stored in `fmt`, and then `fmt` is used to actually format each row.

    # TODO: Consider replacing this with a *real* table formatting tool
    if with_index:
        if with_score:
            fmt = f"{{0: <{rst_width}}}  {{1: ^{score_width}}}  {{2: ^{index_width}}}"
            print(fmt.format("  Name", "Score", "Index"))
            print(fmt.format("-" * rst_width, "-" * score_width, "-" * index_width))
            print("\n".join(fmt.format(*res) for res in results))
        else:
            fmt = f"{{0: <{rst_width}}}  {{1: ^{index_width}}}"
            print(fmt.format("  Name", "Index"))
            print(fmt.format("-" * rst_width, "-" * index_width))
            print("\n".join(fmt.format(*res) for res in results))
    else:
        if with_score:
            fmt = f"{{0: <{rst_width}}}  {{1: ^{score_width}}}"
            print(fmt.format("  Name", "Score"))
            print(fmt.format("-" * rst_width, "-" * score_width))
            print("\n".join(fmt.format(*res) for res in results))
        else:
            print("\n".join(str(res) for res in results))
