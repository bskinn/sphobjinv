r"""*CLI entrypoint for* |soi-textconv|.

|soi| is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

|soi-textconv| is a strictly limited subset of
|soi| expects an INFILE inventory, converts it, then writes to
|stdout|. Intended for use with :code:`git diff`. git, detect
changes, by first converting an (partially binary) inventory to
plain text.

**Author**
    Dave Faulkmore (msftcangoblowme@protonmail.com)

**File Created**
    23 Aug 2024

**Copyright**
    \(c) Brian Skinn 2016-2024

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

**Configure git diff to understand .inv binary files**

Currently there is no CLI command to configure git to recognize
.inv as a binary file and how to convert to plain text.

So, for now, here is the step by step howto

In ``.git/config`` (or $HOME/.config/git/config) append,

.. code-block:: text

   [diff "inv"]
       textconv = [absolute path to venv bin folder]/sphobjinv-textconv

Note not whitespaces, one tab

In ``.gitattributes`` append,

.. code-block:: text

   *.inv binary diff=inv

**Run non local tests**

.. code-block:: shell

   pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
   --cov-config=pyproject.toml --nonloc tests

**Members**

"""

import contextlib
import io
import os
import sys
from unittest.mock import patch

from sphobjinv import Inventory
from sphobjinv.cli.convert import do_convert
from sphobjinv.cli.load import inv_local, inv_stdin, inv_url
from sphobjinv.cli.parser import getparser_textconv, PrsConst


def print_stderr_2(thing, params_b, *, end=os.linesep):
    r"""Bypass parser dependent, print_strerr.

    Use along with :func:`unittest.mock.patch` whenever calling
    sphobjinv.cli internals.

    Parameters
    ----------
    thing

        *any* -- Object to be printed

    params

        |dict| or |None| -- User input parameters/values mapping

    end

        |str| -- String to append to printed content (default: ``\n``\ )

    """
    kwargs = {"file": sys.stderr, "end": end}
    if params_b is None:
        args = (thing,)
    else:
        args = (thing, params_b)

    print(*args, **kwargs)


def _update_with_hardcoded(params):
    r"""In-place (by reference) update parameter dict.

    Configuration will cause :func:`sphobjinv.cli.convert.do_convert`
    to print to |stdout|.

    Parameters
    ----------
    params

        |dict| -- User input parameters/values mapping

    """
    # hardcoded behavior -- print to stdout
    params[PrsConst.OUTFILE] = "-"

    # hardcoded behavior -- inventory --> plain
    params[PrsConst.MODE] = PrsConst.PLAIN

    # hardcoded behavior -- only applies to sphobjinv convert zlib
    # see tests/test_cli TestConvertGood.test_cli_convert_expandcontract
    params[PrsConst.CONTRACT] = False

    # Fallback
    if not hasattr(params, PrsConst.EXPAND):
        params[PrsConst.EXPAND] = False
    else:  # pragma: no cover
        pass


def _wrap_inv_stdin(params):
    """Don't even try to support inventories passed in |stdin|.

    .. code-block:: shell

       sphobjinv convert plain "-" "-" < tests/resource/objects_cclib.inv

    Raises :exc:`UnicodeDecodeError` when receives zlib inventory

    Parameters
    ----------
    params

        |dict| -- User input parameters/values mapping

    Returns
    -------
    status

        |bool| -- True valid inventory received on stdin otherwise False


    Inventory -- either json or plain text

    .. code-block:: shell

       sphobjinv convert plain tests/resource/objects_cclib.inv "-" | sphobjinv-textconv
       sphobjinv convert plain tests/resource/objects_cclib.inv "-" 2>/dev/null | \
       sphobjinv-textconv "-" 2>/dev/null

    """
    f = io.StringIO()
    with patch("sphobjinv.cli.load.print_stderr", wraps=print_stderr_2):
        with contextlib.redirect_stderr(f):
            with contextlib.suppress(SystemExit):
                inv = inv_stdin(params)
        msg_err = f.getvalue().strip()
        f.close()

    is_inv = "inv" in locals() and inv is not None and issubclass(type(inv), Inventory)

    if is_inv:
        # Pipe in json or plain text?! Adapt to survive
        params_b = {}
        in_path = None
        _update_with_hardcoded(params_b)
        # check is inventory file
        do_convert(inv, in_path, params_b)
        ret = True
    else:
        # Not an inventory or a zlib inventory. Move on
        ret = False

    return ret


def main():
    r"""Convert inventory file and print onto |stdout|.

    git requires can accept at most one positional argument, INFILE.
    """
    if len(sys.argv) == 1:
        # zlib inventory --> UnicodeDecodeError is known and unsupported
        params = {}
        # Can exit codes 0 or continues
        is_inv = _wrap_inv_stdin(params)
        if is_inv:
            sys.exit(0)
        else:
            # If no args passed, stick in '-h'
            sys.argv.append("-h")

    prs = getparser_textconv()

    # Parse commandline arguments, discarding any unknown ones
    ns, _ = prs.parse_known_args()
    params = vars(ns)

    # Print version &c. and exit if indicated
    if params[PrsConst.VERSION]:
        print(PrsConst.VER_TXT)
        sys.exit(0)

    # Regardless of mode, insert extra blank line
    # for cosmetics
    print_stderr_2(os.linesep, params)

    # Generate the input Inventory based on --url or stdio or file.
    # These inventory-load functions should call
    # sys.exit(n) internally in error-exit situations
    if params[PrsConst.URL]:
        if params[PrsConst.INFILE] == "-":
            prs.error("argument -u/--url not allowed with '-' as infile")

        # Bypass problematic sphobjinv.cli.ui:print_stderr
        # sphobjinv-textconv --url 'file:///tests/resource/objects_cclib.inv'
        f = io.StringIO()
        with patch("sphobjinv.cli.load.print_stderr", wraps=print_stderr_2):
            with contextlib.redirect_stderr(f):
                with contextlib.suppress(SystemExit):
                    inv, in_path = inv_url(params)
            msg_err = f.getvalue().strip()
            f.close()

        if len(msg_err) != 0 and msg_err.startswith("Error: URL mode"):
            print_stderr_2(msg_err, None)
            sys.exit(1)
    elif params[PrsConst.INFILE] == "-":
        """
        sphobjinv convert plain tests/resource/objects_cclib.inv "-" 2>/dev/null | \
        sphobjinv-textconv "-" 2>/dev/null
        """
        try:
            is_inv = _wrap_inv_stdin(params)
        except UnicodeDecodeError:
            """Piping in a zlib inventory is not supported

            In :func:`sphobjinv.cli.load.inv_stdin`, a call to
            :func:`sys.stdin.read` raises an uncaught exception which
            propagates up the stack and the traceback is displayed to
            the end user.

            This is bad UX

            Place the call within a try-except block. The function should
            raise one, not two, custom exception. Handling zlib inventory
            and non-inventory for an empty file

            .. code-block:: shell

               sphobjinv-textconv "-" \
               2>/dev/null < plain tests/resource/objects_cclib.inv
               echo $?

            1

            """
            msg_err = "Invalid plaintext or JSON inventory format."
            print_stderr_2(msg_err, None)
            sys.exit(1)
        else:
            if is_inv:
                # Cosmetic final blank line
                print_stderr_2(os.linesep, params)
                sys.exit(0)
            else:  # pragma: no cover
                # No inventory
                pass
    else:
        inv, in_path = inv_local(params)

    is_in_path = "in_path" in locals() and in_path is not None
    if is_in_path:
        _update_with_hardcoded(params)

        # check is inventory file
        do_convert(inv, in_path, params)

        # Cosmetic final blank line
        print_stderr_2(os.linesep, params)
    else:  # pragma: no cover
        # No inventory
        pass

    # Clean exit
    sys.exit(0)
