r"""*Nonlocal CLI tests for* ``sphobjinv-textconv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

``sphobjinv-textconv`` is a strictly limited subset of
``sphobjinv`` expects an INFILE inventory, converts it, then writes to
stdout. Intended for use with git diff. git, detect changes, by first
converting an (partially binary) inventory to plain text.

**Author**
    Dave Faulkmore (msftcangoblowme@protonmail.com)

**File Created**
    24 Aug 2024

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

import pytest
from stdio_mgr import stdio_mgr
from tests.enum import Entrypoints

CLI_TEST_TIMEOUT = 5

pytestmark = [pytest.mark.cli, pytest.mark.nonloc]


class TestTextconvOnlineBad:
    """Tests for textconv, online, expected-fail behaviors."""

    @pytest.mark.parametrize(
        "url, runargs, expected, msg",
        (
            (
                "http://sphobjinv.readthedocs.io/en/v2.0/objects.inv",
                ["-e", "--url", "-"],
                2,
                "argument -u/--url not allowed with '-' as infile",
            ),
        ),
        ids=["both --url and infile '-' do allowed"],
    )
    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_textconv_both_url_and_infile(
        self,
        url,
        runargs,
        expected,
        msg,
        run_cmdline_test,
    ):
        """Online URL and INFILE "-", cannot specify both.

        .. code-block:: shell

           pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
           --cov-config=pyproject.toml -k test_textconv_both_url_and_infile tests

        """
        # Both --url and INFILE "-". Excess args are discarded.
        # In this case INFILE "-"
        # For this test, URL cannot be local (file:///)
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(runargs, expect=expected, prog=Entrypoints.SOI_TEXTCONV)
            str_err = err_.getvalue()
            assert msg in str_err


class TestTextconvOnlineGood:
    """Tests for textconv, online, expected-good functionality."""

    @pytest.mark.parametrize(
        "url, expected_retcode",
        (
            (
                "http://sphobjinv.readthedocs.io/en/v2.0/objects.inv",
                0,
            ),
        ),
        ids=["Remote zlib inventory URL"],
    )
    @pytest.mark.timeout(CLI_TEST_TIMEOUT * 4)
    def test_textconv_online_url(
        self,
        url,
        expected_retcode,
        run_cmdline_test,
    ):
        """Valid nonlocal url."""
        runargs = ["--url", url]
        run_cmdline_test(
            runargs,
            expect=expected_retcode,
            prog=Entrypoints.SOI_TEXTCONV,
        )
