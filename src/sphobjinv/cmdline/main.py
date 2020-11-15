r"""``sphobjinv`` *CLI main execution module*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    15 Nov 2020

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

import sys

from sphobjinv.cmdline.parser import getparser

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
