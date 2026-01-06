r"""*Textconv CLI tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    22 Dec 2025

**Copyright**
    \(c) Brian Skinn 2016-2025

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

**Members**

"""

import re
import shlex
import subprocess as sp  # noqa: S404
from pathlib import Path

import pytest
from stdio_mgr import stdio_mgr

from sphobjinv import Inventory
from tests.enum import CLICommand

CLI_TEST_TIMEOUT = 2
CLI_CMDS = ["sphobjinv-textconv"]

pytestmark = [pytest.mark.cli, pytest.mark.textconv, pytest.mark.local]


class TestMisc:
    """Tests for miscellaneous textconv entrypoint behavior."""

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    @pytest.mark.parametrize("cmd", CLI_CMDS)
    def test_cli_invocations(self, cmd):
        """Confirm that actual shell invocations do not error."""
        runargs = shlex.split(cmd)
        runargs.append("--help")

        out = sp.check_output(" ".join(runargs), shell=True).decode()  # noqa: S602

        assert "sphobjinv" in out
        assert "infile" in out

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_cli_version_exits_ok(self, run_cmdline_test):
        """Confirm --version exits cleanly."""
        run_cmdline_test(["-v"], command=CLICommand.Textconv)

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_cli_noargs_shows_help(self, run_cmdline_test):
        """Confirm help shown when invoked with no arguments."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test([], command=CLICommand.Textconv)

            assert re.search("usage.+sphobjinv", out_.getvalue(), re.I)


class TestGood:
    """Tests for expected-good textconv entrypoint functionality."""

    def test_textconv_matches_main_conv(self, res_cmp, run_cmdline_test):
        """Ensure that textconv conversion matches main CLI conversion."""
        with stdio_mgr() as (_, out_, _):
            run_cmdline_test(
                ["convert", "plain", res_cmp, "-"], command=CLICommand.Core
            )
            core_output = out_.getvalue()

        with stdio_mgr() as (_, out_, _):
            run_cmdline_test([res_cmp], command=CLICommand.Textconv)
            textconv_output = out_.getvalue()

        assert core_output == textconv_output

    def test_textconv_matches_original(self, res_cmp, run_cmdline_test):
        """Confirm textconv produces a consistent Inventory."""
        with stdio_mgr() as (_, out_, _):
            run_cmdline_test([str(res_cmp.resolve())], command=CLICommand.Textconv)

            result = out_.getvalue()

        inv1 = Inventory(res_cmp)
        inv2 = Inventory(result.encode("utf-8"))

        assert inv1 == inv2


class TestFail:
    """Tests for expected-fail textconv entrypoint behaviors."""

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_wrongfiletype(
        self, scratch_path, run_cmdline_test, monkeypatch
    ):
        """Confirm exit code 1 with invalid file format."""
        monkeypatch.chdir(scratch_path)
        fname = "testfile"
        Path(fname).write_bytes(b"this is not objects.inv\n")

        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test([fname], command=CLICommand.Textconv, expect=1)
            assert "Unrecognized" in err_.getvalue()

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_missingfile(self, run_cmdline_test):
        """Confirm exit code 1 with nonexistent file specified."""
        run_cmdline_test(
            ["thisfileshouldbeabsent.txt"], command=CLICommand.Textconv, expect=1
        )

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_outputdir_provided(
        self, res_cmp, scratch_path, run_cmdline_test
    ):
        """Confirm exit code 2 when too many inputs are provided."""
        run_cmdline_test(
            [
                res_cmp,
                str(scratch_path / "objects.txt"),
            ],
            command=CLICommand.Textconv,
            expect=2,
        )

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_pathonlysrc(self, scratch_path, run_cmdline_test):
        """Confirm cmdline plaintext convert with input directory arg fails."""
        run_cmdline_test(
            [str(scratch_path)],
            command=CLICommand.Textconv,
            expect=1,
        )

    def test_clifail_no_url_arg(self, run_cmdline_test):
        """Confirm textconv parser errors on non-existent -u flag."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                ["-u", "nofile.inv"], command=CLICommand.Textconv, expect=2
            )
            assert "unrecognized argument" in err_.getvalue()
