r"""*Nonlocal CLI tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    20 Mar 2019

**Copyright**
    \(c) Brian Skinn 2016-2020

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**
"""


import json
import re

import pytest
from stdio_mgr import stdio_mgr

from sphobjinv import Inventory

CLI_TEST_TIMEOUT = 5

p_instance_of = re.compile("^.*instance_of.*$", re.M)
p_inventory = re.compile("^.*nventory.*$", re.I | re.M)

pytestmark = [pytest.mark.cli, pytest.mark.nonloc]


@pytest.fixture(scope="module", autouse=True)
def skip_if_no_nonloc(pytestconfig):
    """Skip test if --nonloc not provided.

    Auto-applied to all functions in module, since module is nonlocal.

    """
    if not pytestconfig.getoption("--nonloc"):
        pytest.skip("'--nonloc' not specified")  # pragma: no cover


class TestConvert:
    """Test nonlocal CLI convert mode functionality."""

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_cli_convert_from_url_with_dest(
        self, scratch_path, misc_info, run_cmdline_test, monkeypatch
    ):
        """Confirm CLI URL D/L, convert works w/outfile supplied."""
        monkeypatch.chdir(scratch_path)

        dest_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.DEC)
        run_cmdline_test(
            [
                "convert",
                "plain",
                "-u",
                misc_info.remote_url.format("attrs"),
                str(dest_path),
            ]
        )

        assert dest_path.is_file()

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_cli_convert_from_url_no_dest(
        self, scratch_path, misc_info, run_cmdline_test, monkeypatch
    ):
        """Confirm CLI URL D/L, convert works w/o outfile supplied."""
        monkeypatch.chdir(scratch_path)
        dest_path = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.DEC)
        dest_path.unlink()
        run_cmdline_test(
            ["convert", "plain", "-u", misc_info.remote_url.format("attrs")]
        )
        assert dest_path.is_file()

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_cli_url_in_json(
        self, scratch_path, misc_info, run_cmdline_test, monkeypatch
    ):
        """Confirm URL is present when using CLI URL mode."""
        monkeypatch.chdir(scratch_path)
        dest_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.JSON)
        run_cmdline_test(
            [
                "convert",
                "json",
                "-u",
                misc_info.remote_url.format("attrs"),
                str(dest_path.resolve()),
            ]
        )

        d = json.loads(dest_path.read_text())

        assert "objects" in d.get("metadata", {}).get("url", {})

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_clifail_bad_url(self, run_cmdline_test, misc_info, scratch_path):
        """Confirm proper error behavior when a bad URL is passed."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                [
                    "convert",
                    "plain",
                    "-u",
                    misc_info.remote_url.format("blarghers"),
                    str(scratch_path),
                ],
                expect=1,
            )
            assert "No inventory at provided URL." in err_.getvalue()

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_clifail_url_no_leading_http(self, run_cmdline_test, scratch_path):
        """Confirm proper error behavior when a URL w/o leading 'http://' is passed."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                [
                    "convert",
                    "plain",
                    "-u",
                    "sphobjinv.readthedocs.io/en/latest",
                    str(scratch_path),
                ],
                expect=1,
            )
            assert "No inventory at provided URL." in err_.getvalue()

    def test_cli_json_export_import(
        self, res_cmp, scratch_path, misc_info, run_cmdline_test, sphinx_load_test
    ):
        """Confirm JSON sent to stdout from local source imports ok."""
        inv_url = misc_info.remote_url.format("attrs")
        mod_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.CMP)

        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(["convert", "json", "-u", inv_url, "-"])

            data = out_.getvalue()

        with stdio_mgr(data) as (in_, out_, err_):
            run_cmdline_test(["convert", "zlib", "-", str(mod_path.resolve())])

        assert Inventory(json.loads(data))
        assert Inventory(mod_path)
        sphinx_load_test(mod_path)


class TestSuggest:
    """Test nonlocal CLI suggest mode functionality."""

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_cli_suggest_from_url(self, misc_info, run_cmdline_test):
        """Confirm name-only suggest works from URL."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                [
                    "suggest",
                    "-u",
                    misc_info.remote_url.format("attrs"),
                    "instance",
                    "-t",
                    "50",
                ]
            )
            assert p_instance_of.search(out_.getvalue())

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_cli_suggest_from_dir_noanchor(self, run_cmdline_test):
        """Confirm name-only suggest works from docpage URL."""
        url = "http://sphobjinv.readthedocs.io/en/v2.0/modules/"
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(["suggest", "-u", url, "inventory", "-at", "50"])
            assert p_inventory.search(out_.getvalue())

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_cli_suggest_from_page_noanchor(self, run_cmdline_test):
        """Confirm name-only suggest works from docpage URL."""
        url = "http://sphobjinv.readthedocs.io/en/v2.0/modules/cmdline.html"
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(["suggest", "-u", url, "inventory", "-at", "50"])
            assert p_inventory.search(out_.getvalue())

    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_cli_suggest_from_page_withanchor(self, run_cmdline_test):
        """Confirm name-only suggest works from docpage URL."""
        url = (
            "http://sphobjinv.readthedocs.io/en/v2.0/modules/"
            "cmdline.html#sphobjinv.cmdline.do_convert"
        )
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(["suggest", "-u", url, "inventory", "-at", "50"])
            assert p_inventory.search(out_.getvalue())
