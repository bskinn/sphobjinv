r"""*Nonlocal CLI tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    20 Mar 2019

**Copyright**
    \(c) Brian Skinn 2016-2019

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**
"""

import os
import os.path as osp
import re
import unittest as ut

try:
    from signal import SIGALRM

    SIGALRM  # Placate flake8
except ImportError:
    # Probably running on Windows; timeout-decorator won't work
    def timeout(dummy_sec):
        """Decorate the function with a null transform."""

        def null_dec(func):
            return func

        return null_dec


else:
    from timeout_decorator import timeout


from .sphobjinv_base import DEC_EXT, CMP_EXT, JSON_EXT
from .sphobjinv_base import INIT_FNAME_BASE, MOD_FNAME_BASE
from .sphobjinv_base import RES_FNAME_BASE
from .sphobjinv_base import INVALID_FNAME, TESTALL
from .sphobjinv_base import REMOTE_URL
from .sphobjinv_base import SuperSphobjinv
from .sphobjinv_base import copy_dec, copy_cmp, scr_path, res_path
from .sphobjinv_base import copy_json
from .sphobjinv_base import decomp_cmp_test, file_exists_test
from .sphobjinv_base import run_cmdline_test, sphinx_load_test
from .sphobjinv_base import dir_change
from stdio_mgr import stdio_mgr


CLI_TIMEOUT = 2



from time import sleep

import pytest

CLI_TEST_TIMEOUT = 2


pytestmark = [pytest.mark.cli, pytest.mark.nonloc]


@pytest.mark.skip("Un-converted tests")
class TestSphobjinvCmdlineExpectGoodNonlocal(SuperSphobjinv, ut.TestCase):
    """Testing nonlocal code expecting to work properly."""

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_SuggestNameOnlyFromInventoryURL(self):
        """Confirm name-only suggest works from URL."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                self,
                ["suggest", "-u", REMOTE_URL.format("attrs"), "instance", "-t", "50"],
            )

            p = re.compile("^.*instance_of.*$", re.M)

            with self.subTest("found_object"):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_SuggestNameOnlyFromDirURLNoAnchor(self):
        """Confirm name-only suggest works from docpage URL."""
        URL = "http://sphobjinv.readthedocs.io/en/v2.0rc1/" "modules/"

        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ["suggest", "-u", URL, "inventory", "-at", "50"])

            p = re.compile("^.*nventory.*$", re.I | re.M)

            with self.subTest("found_object"):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_SuggestNameOnlyFromPageURLNoAnchor(self):
        """Confirm name-only suggest works from docpage URL."""
        URL = "http://sphobjinv.readthedocs.io/en/v2.0rc1/" "modules/cmdline.html"

        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ["suggest", "-u", URL, "inventory", "-at", "50"])

            p = re.compile("^.*nventory.*$", re.I | re.M)

            with self.subTest("found_object"):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_SuggestNameOnlyFromPageURLWithAnchor(self):
        """Confirm name-only suggest works from docpage URL."""
        URL = (
            "http://sphobjinv.readthedocs.io/en/v2.0rc1/modules/"
            "cmdline.html#sphobjinv.cmdline.do_convert"
        )

        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ["suggest", "-u", URL, "inventory", "-at", "50"])

            p = re.compile("^.*nventory.*$", re.I | re.M)

            with self.subTest("found_object"):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_ConvertURLToPlaintextOutfileProvided(self):
        """Confirm CLI URL D/L, convert works w/outfile supplied."""
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(
            self, ["convert", "plain", "-u", REMOTE_URL.format("attrs"), dest_path]
        )

        file_exists_test(self, dest_path)

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_ConvertURLToPlaintextNoOutfile(self):
        """Confirm CLI URL D/L, convert works w/o outfile supplied."""
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        with dir_change("sphobjinv"):
            with dir_change("test"):
                with dir_change("scratch"):
                    run_cmdline_test(
                        self, ["convert", "plain", "-u", REMOTE_URL.format("attrs")]
                    )

        file_exists_test(self, dest_path)



@pytest.mark.skip("Un-converted tests")
class TestSphobjinvCmdlineExpectFailNonlocal(SuperSphobjinv, ut.TestCase):
    """Check expect-fail cases with non-local sources/effects."""

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_BadURLArg(self):
        """Confirm proper error behavior when a bad URL is passed."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                self,
                ["convert", "plain", "-u", REMOTE_URL.format("blarghers"), scr_path()],
                expect=1,
            )

            with self.subTest("stdout_match"):
                self.assertIn("No inventory at provided URL.", out_.getvalue())

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_NotSphinxURLArg(self):
        """Confirm proper error behavior when a non-Sphinx URL is passed."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                self,
                ["convert", "plain", "-u", "http://www.google.com", scr_path()],
                expect=1,
            )

            with self.subTest("stdout_match"):
                self.assertIn("No inventory at provided URL.", out_.getvalue())

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_NoHTTPURLArg(self):
        """Confirm proper error behavior when a non-Sphinx URL is passed."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                self,
                [
                    "convert",
                    "plain",
                    "-u",
                    "sphobjinv.readthedocs.io/en/latest",
                    scr_path(),
                ],
                expect=1,
            )

            with self.subTest("stdout_match"):
                self.assertIn("No inventory at provided URL.", out_.getvalue())



if __name__ == "__main__":
    print("Module not executable.")
