# ------------------------------------------------------------------------------
# Name:        sphobjinv_cli
# Purpose:     Module for sphobjinv command line tests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     18 Dec 2017
# Copyright:   (c) Brian Skinn 2016-2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Module for sphobjinv command line tests."""

import os
import os.path as osp
import unittest as ut

from .sphobjinv_base import DEC_EXT, ENC_EXT
from .sphobjinv_base import INIT_FNAME_BASE, MOD_FNAME_BASE
from .sphobjinv_base import INVALID_FNAME
from .sphobjinv_base import SuperSphobjinv
from .sphobjinv_base import copy_dec, copy_enc, scr_path
from .sphobjinv_base import decomp_cmp_test, file_exists_test
from .sphobjinv_base import run_cmdline_test, sphinx_load_test
from .sphobjinv_base import dir_change


class TestSphobjinvCmdlineExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_CmdlineDecodeNoArgs(self):
        """Confirm commandline decode exec with no args succeeds."""
        copy_enc()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['decode'])

                    file_exists_test(self, INIT_FNAME_BASE + DEC_EXT)

                    decomp_cmp_test(self, INIT_FNAME_BASE + DEC_EXT)

    def test_CmdlineEncodeNoArgs(self):
        """Confirm commandline encode exec with no args succeeds."""
        copy_dec()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['encode'])

                    file_exists_test(self, INIT_FNAME_BASE + ENC_EXT)

                    sphinx_load_test(self, INIT_FNAME_BASE + ENC_EXT)

    def test_CmdlineDecodeSrcFile(self):
        """Confirm cmdline decode with input file arg."""
        copy_enc()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['decode',
                                scr_path(INIT_FNAME_BASE + ENC_EXT)])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    def test_CmdlineEncodeSrcFile(self):
        """Confirm cmdline encode with input file arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + ENC_EXT)
        run_cmdline_test(self, ['encode',
                                scr_path(INIT_FNAME_BASE + DEC_EXT)])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    def test_CmdlineDecodeSrcPath(self):
        """Confirm cmdline decode with input directory arg."""
        copy_enc()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['decode', scr_path()])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    def test_CmdlineEncodeSrcPath(self):
        """Confirm cmdline encode with input directory arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + ENC_EXT)
        run_cmdline_test(self, ['encode', scr_path()])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    def test_CmdlineDecodeTgtNewName(self):
        """Confirm cmdline decode to custom target name in same dir."""
        copy_enc()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['decode', '-', dest_fname])

                    file_exists_test(self, dest_fname)

                    decomp_cmp_test(self, dest_fname)

    def test_CmdlineEncodeTgtNewName(self):
        """Confirm cmdline encode to custom target name in same dir."""
        copy_dec()
        dest_fname = MOD_FNAME_BASE + ENC_EXT
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['encode', '.', dest_fname])

                    file_exists_test(self, dest_fname)

                    sphinx_load_test(self, dest_fname)

    def test_CmdlineDecodeDiffSrcPathNewNameThere(self):
        """Confirm decode in other path outputs there if only name passed."""
        copy_enc()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        run_cmdline_test(self, ['decode', scr_path(), dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        decomp_cmp_test(self, scr_path(dest_fname))

    def test_CmdlineEncodeDiffSrcPathNewNameThere(self):
        """Confirm encode in other path outputs there if only name passed."""
        copy_dec()
        dest_fname = MOD_FNAME_BASE + ENC_EXT
        run_cmdline_test(self, ['encode', scr_path(), dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        sphinx_load_test(self, scr_path(dest_fname))

    def test_CmdlineDecodeDiffSrcTgtPaths(self):
        """Confirm decode from other path to new path."""
        copy_enc()
        dest_path = osp.join(os.curdir, MOD_FNAME_BASE + DEC_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['decode', os.pardir, dest_path])

                        file_exists_test(self, dest_path)

                        decomp_cmp_test(self, dest_path)

    def test_CmdlineEncodeDiffSrcTgtPaths(self):
        """Confirm encode from other path to new path."""
        copy_dec()
        dest_path = osp.join(os.curdir, MOD_FNAME_BASE + ENC_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['encode', os.pardir, dest_path])

                        file_exists_test(self, dest_path)

                        sphinx_load_test(self, dest_path)

    def test_CmdlineDecodeTgtBarePath(self):
        """Confirm decode to target as bare path."""
        copy_enc()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['decode', os.pardir, '.'])

                        file_exists_test(self, INIT_FNAME_BASE + DEC_EXT)

                        decomp_cmp_test(self, INIT_FNAME_BASE + DEC_EXT)

    def test_CmdlineEncodeTgtBarePath(self):
        """Confirm encode to target as bare path."""
        copy_dec()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['encode', os.pardir, '.'])

                        file_exists_test(self, INIT_FNAME_BASE + ENC_EXT)

                        sphinx_load_test(self, INIT_FNAME_BASE + ENC_EXT)


class TestSphobjinvCmdlineExpectFail(SuperSphobjinv, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    def test_CmdlineDecodeWrongFileType(self):
        """Confirm exit code 1 with invalid file format."""
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    fname = 'testfile'
                    with open(fname, 'wb') as f:
                        f.write(b'this is not objects.inv\n')

                    run_cmdline_test(self,
                                     ['decode', fname],
                                     expect=1)

    def test_CmdlineDecodeMissingFile(self):
        """Confirm exit code 1 with nonexistent file specified."""
        run_cmdline_test(self, ['decode', 'thisfileshouldbeabsent.txt'],
                         expect=1)

    def test_CmdlineDecodeBadOutputFilename(self):
        """Confirm exit code 1 with invalid output file name."""
        copy_enc()
        run_cmdline_test(self,
                         ['decode',
                          scr_path(INIT_FNAME_BASE + ENC_EXT),
                          INVALID_FNAME],
                         expect=1)


def suite_cli_expect_good():
    """Create and return the test suite for CLI expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvCmdlineExpectGood)])

    return s


def suite_cli_expect_fail():
    """Create and return the test suite for CLI expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvCmdlineExpectFail)])

    return s


if __name__ == '__main__':
    print("Module not executable.")
