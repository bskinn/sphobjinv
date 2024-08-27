r"""*CLI tests for* ``sphobjinv-textconv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

``sphobjinv-textconv`` is a strictly limited subset of
``sphobjinv`` expects an INFILE inventory, converts it, then writes to
stdout. Intended for use with git diff. git, detect changes, by first
converting an (partially binary) inventory to plain text.

**Author**
    Dave Faulkmore (msftcangoblowme@protonmail.com)

**File Created**
    23 Aug 2024

**Copyright**
    \(c) Brian Skinn 2016-2024

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

.. code-block:: shell

   pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
   --cov-config=pyproject.toml --nonloc tests

**Members**

"""


import json
import os
import shlex
import subprocess as sp  # noqa: S404
import sys
from pathlib import Path

import pytest
from stdio_mgr import stdio_mgr

from sphobjinv import Inventory
from sphobjinv import SourceTypes
from sphobjinv.fileops import readbytes

CLI_TEST_TIMEOUT = 2
# Is an entrypoint, but not a package
CLI_CMDS = ["sphobjinv-textconv"]

pytestmark = [pytest.mark.cli, pytest.mark.local]


@pytest.fixture
def windows_paths():
    """Fixture prints diagnostic info for bugging Windows paths."""
    import os
    import site

    def func() -> None:
        """Diagnostic info for bugging Windows paths."""
        # On Windows what is the bin path?
        print(f"""VIRTUAL_ENV: {os.environ['VIRTUAL_ENV']}""", file=sys.stderr)
        # On Windows, what is the lib path?
        # /home/faulkmore/.local/lib/python3.9/site-packages
        print(f"Packages site path: {site.USER_SITE}", file=sys.stderr)

    return func


class TestTextconvMisc:
    """Tests for miscellaneous CLI functions."""

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    @pytest.mark.parametrize("cmd", CLI_CMDS)
    def test_cli_textconv_help(self, cmd, run_cmdline_no_checks):
        """Confirm that actual shell invocations do not error.

        .. code-block:: shell

           pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
           --cov-config=pyproject.toml -k test_cli_textconv_help tests

        """
        runargs = shlex.split(cmd)
        runargs.append("--help")

        with stdio_mgr() as (in_, out_, err_):
            retcode, is_sys_exit = run_cmdline_no_checks(runargs)
            str_out = out_.getvalue()
            assert "sphobjinv-textconv" in str_out

            # Ideally, the only place sys.exit calls occur within a codebase is in
            # entrypoint file(s). In this case, sphobjinv.cli.core
            #
            # Each unique custom Exception has a corresponding unique exit code.
            #
            # Testing looks at exit codes only.
            #
            # Not the error messages, which could change or be localized
            #
            # In command line utilities, relaying possible errors is common practice
            #
            # From an UX POV, running echo $? and getting 1 on error is
            # useless and frustrating.
            #
            # Not relaying errors and giving exact feedback on how to rectify
            # the issue is bad UX.
            #
            # So if the numerous exit codes of 1 looks strange. It is; but this is
            # a separate issue best solved within a dedicated commit
            assert f"EXIT CODES{os.linesep}" in str_out

            # Leave zero doubt about
            #
            # - what it's for
            # - how to use
            # - what to expect
            assert f"USAGE{os.linesep}" in str_out

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_cli_version_exits_ok(self, run_cmdline_textconv):
        """Confirm --version exits cleanly."""
        run_cmdline_textconv(["-v"])

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_cli_noargs_shows_help(self, run_cmdline_textconv):
        """Confirm help shown when invoked with no arguments."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_textconv([])
            str_out = out_.getvalue()
            assert "usage: sphobjinv-textconv" in str_out


class TestTextconvGood:
    """Tests for expected-good textconv functionality."""

    @pytest.mark.parametrize(
        "in_ext", [".txt", ".inv", ".json"], ids=(lambda i: i.split(".")[-1])
    )
    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_cli_textconv_inventory_files(
        self,
        in_ext,
        scratch_path,
        run_cmdline_textconv,
        misc_info,
    ):
        """Inventory files' path provided via cli. stdout is not captured."""
        src_path = scratch_path / (misc_info.FNames.INIT + in_ext)

        assert src_path.is_file()

        cli_arglist = [str(src_path)]

        # Confirm success, but sadly no stdout
        run_cmdline_textconv(cli_arglist)

        # More than one positional arg. Expect additional positional arg to be ignored
        cli_arglist = [str(src_path), "7"]
        run_cmdline_textconv(cli_arglist)

        # Unknown keyword arg. Expect to be ignored
        cli_arglist = [str(src_path), "--elephant-shoes", "42"]
        run_cmdline_textconv(cli_arglist)


class TestTextconvFail:
    """Tests for textconv expected-fail behaviors."""

    def test_cli_textconv_url_bad(
        self,
        scratch_path,
        misc_info,
        run_cmdline_textconv,
        run_cmdline_no_checks,
    ):
        """Confirm cmdline contract. Confirm local inventory URLs not allowed."""
        path_cmp = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.CMP)

        # --url instead of infile. local url not allowed
        url_local_path = f"""file://{path_cmp!s}"""
        run_cmdline_textconv(["-e", "--url", url_local_path], expect=1)


@pytest.mark.parametrize(
    "data_format",
    [SourceTypes.DictJSON, SourceTypes.BytesPlaintext],
    ids=["json", "plaintext"],
)
def test_cli_textconv_via_subprocess(
    data_format,
    res_dec,
    res_cmp,
    misc_info,
    windows_paths,
):
    """In a subprocess, plain inventory passed in thru stdin.

    .. code-block:: shell

       pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
       --cov-config=pyproject.toml -k test_cli_textconv_via_subprocess tests

    """
    # prepare
    retcode_expected = 0

    windows_paths()

    path_cmd = Path(sys.executable).parent.joinpath("sphobjinv-textconv")
    cmd_path = str(path_cmd)

    inv1 = Inventory(res_cmp)
    if data_format is SourceTypes.DictJSON:
        input_data = json.dumps(inv1.json_dict())
    elif data_format is SourceTypes.BytesPlaintext:
        input_data = inv1.data_file().decode("utf-8")

    expected = inv1.data_file().decode("utf-8")

    # Act
    cmds = (
        [cmd_path],
        [cmd_path, "-"],
    )
    for cmd in cmds:
        try:
            p_result = sp.run(
                cmd,
                shell=False,  # noqa: S603
                input=input_data,
                text=True,
                capture_output=True,
            )
        except (sp.CalledProcessError, sp.TimeoutExpired):
            pytest.xfail()
        else:
            out = p_result.stdout
            retcode = p_result.returncode
            strlen_out = len(out)
            strlen_in = len(expected)
            # inventory file contains an additional newline
            assert retcode == retcode_expected
            assert strlen_in == strlen_out - 1


class TestTextconvStdioFail:
    """Piping in via stdin expect-fail behaviors."""

    def test_cli_textconv_zlib_inv_stdin(
        self,
        res_cmp,
        windows_paths,
    ):
        """Piping in a zlib inventory is not supported.

        .. code-block:: shell

            sphobjinv-textconv "-" 2>/dev/null < tests/resource/objects_cclib.inv
            echo $?

        1

        Run this test class method

        .. code-block:: shell

           pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
           --cov-config=pyproject.toml -k test_cli_textconv_zlib_inv_stdin tests

        """
        expected_retcode = 1

        # prepare
        #    byte stream usable by subprocess
        bytes_cmp = readbytes(res_cmp)

        windows_paths()

        path_cmd = Path(sys.executable).parent.joinpath("sphobjinv-textconv")
        cmd_path = str(path_cmd)

        cmd = [cmd_path, "-"]
        try:
            sp.run(
                cmd,
                shell=False,  # noqa: S603
                input=bytes_cmp,
                text=False,
                capture_output=True,
                check=True,
            )
        except sp.CalledProcessError as e:
            retcode = e.returncode
            b_err = e.stderr
            str_err = b_err.decode("utf-8")
            assert retcode == expected_retcode
            assert "Invalid plaintext or JSON inventory format." in str_err
        else:
            reason = (
                "Piping in zlib inventory via stdin is not supported. "
                "Was expecting exit code 1"
            )
            pytest.xfail(reason)
