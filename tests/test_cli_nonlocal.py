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


import re

import pytest
from stdio_mgr import stdio_mgr


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


# ====  NONLOCAL CONVERT TESTS  ====


@pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
def test_cli_convert_from_url_with_dest(
    scratch_path, misc_info, run_cmdline_test, monkeypatch
):
    """Confirm CLI URL D/L, convert works w/outfile supplied."""
    monkeypatch.chdir(scratch_path)

    dest_path = scratch_path / (
        misc_info.FNames.MOD.value + misc_info.Extensions.DEC.value
    )
    run_cmdline_test(
        ["convert", "plain", "-u", misc_info.remote_url.format("attrs"), str(dest_path)]
    )

    assert dest_path.is_file()


@pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
def test_cli_convert_from_url_no_dest(
    scratch_path, misc_info, run_cmdline_test, monkeypatch
):
    """Confirm CLI URL D/L, convert works w/o outfile supplied."""
    monkeypatch.chdir(scratch_path)
    dest_path = scratch_path / (
        misc_info.FNames.INIT.value + misc_info.Extensions.DEC.value
    )
    dest_path.unlink()
    run_cmdline_test(["convert", "plain", "-u", misc_info.remote_url.format("attrs")])
    assert dest_path.is_file()


@pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
def test_clifail_bad_url(run_cmdline_test, misc_info, scratch_path):
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
        assert "No inventory at provided URL." in out_.getvalue()


@pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
def test_clifail_url_no_leading_http(run_cmdline_test, scratch_path):
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
        assert "No inventory at provided URL." in out_.getvalue()


# ====  NONLOCAL SUGGEST TESTS  ====


@pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
def test_cli_suggest_from_url(misc_info, run_cmdline_test):
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
def test_cli_suggest_from_dir_noanchor(run_cmdline_test):
    """Confirm name-only suggest works from docpage URL."""
    url = "http://sphobjinv.readthedocs.io/en/v2.0/modules/"
    with stdio_mgr() as (in_, out_, err_):
        run_cmdline_test(["suggest", "-u", url, "inventory", "-at", "50"])
        assert p_inventory.search(out_.getvalue())


@pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
def test_cli_suggest_from_page_noanchor(run_cmdline_test):
    """Confirm name-only suggest works from docpage URL."""
    url = "http://sphobjinv.readthedocs.io/en/v2.0/modules/cmdline.html"
    with stdio_mgr() as (in_, out_, err_):
        run_cmdline_test(["suggest", "-u", url, "inventory", "-at", "50"])
        assert p_inventory.search(out_.getvalue())


@pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
def test_cli_suggest_from_page_withanchor(run_cmdline_test):
    """Confirm name-only suggest works from docpage URL."""
    url = (
        "http://sphobjinv.readthedocs.io/en/v2.0/modules/"
        "cmdline.html#sphobjinv.cmdline.do_convert"
    )
    with stdio_mgr() as (in_, out_, err_):
        run_cmdline_test(["suggest", "-u", url, "inventory", "-at", "50"])
        assert p_inventory.search(out_.getvalue())
