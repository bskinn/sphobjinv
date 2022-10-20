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
from sphobjinv.cli.ui import log_print, yesno_prompt


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

    log_print(f"{inv.count} objects in inventory.\n", params)

    if len(results) == 0:
        log_print(
            (
                "No results found with score at/above current threshold of "
                f"{params[PrsConst.THRESH]}."
            ),
            params,
        )
        return
    else:
        log_print(
            (
                f"{len(results)} result"
                f"{'' if len(results) == 1 else 's'}"
                " found at/above current threshold of "
                f"{params[PrsConst.THRESH]}.\n"
            ),
            params,
        )

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
