# ------------------------------------------------------------------------------
# Name:        sphobjinv_cli
# Purpose:     Module for sphobjinv command line tests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     18 Dec 2017
# Copyright:   (c) Brian Skinn 2016-2018
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Module for sphobjinv command line tests."""

import os
import os.path as osp
import unittest as ut

from .sphobjinv_base import DEC_EXT, CMP_EXT, FLAT_EXT, STRUCT_EXT
from .sphobjinv_base import INIT_FNAME_BASE, MOD_FNAME_BASE
from .sphobjinv_base import INVALID_FNAME, TESTALL
from .sphobjinv_base import SuperSphobjinv
from .sphobjinv_base import copy_dec, copy_cmp, scr_path, res_path
from .sphobjinv_base import copy_flat, copy_struct
from .sphobjinv_base import decomp_cmp_test, file_exists_test
from .sphobjinv_base import run_cmdline_test, sphinx_load_test
from .sphobjinv_base import dir_change


class TestSphobjinvCmdlineExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_CmdlineZlibToPlaintextSrcFileOnly(self):
        """Confirm cmdline decompress of zlib with input file arg."""
        copy_cmp()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + CMP_EXT)])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    def test_CmdlineFlatJSONToPlaintextSrcFileOnly(self):
        """Confirm cmdline convert of flat JSON with input file arg."""
        copy_flat()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + FLAT_EXT)])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    def test_CmdlineStructJSONToPlaintextSrcFileOnly(self):
        """Confirm cmdline convert of struct JSON with input file arg.

        Direct file contents comparison test not possible since struct-JSON
        does not retain ordering of the inventory objects.

        """
        copy_struct()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + STRUCT_EXT)])

        file_exists_test(self, dest_path)

    # #### More tests here for each combination of format conversion! ####

    def test_CmdlinePlaintextTgtNewName(self):
        """Confirm cmdline plaintext convert to custom target name in same dir."""
        copy_cmp()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['convert', 'plain',
                                            INIT_FNAME_BASE + CMP_EXT,
                                            dest_fname])

                    file_exists_test(self, dest_fname)

                    decomp_cmp_test(self, dest_fname)

    def test_CmdlineCycleConvert(self):
        """Confirm conversion in a loop, reading all formats."""
        import re

        src_fname = res_path('objects_{0}.inv')
        plain_fname = scr_path('objects_{0}.txt')
        json_fname = scr_path('objects_{0}.flatjson')
        struct_fname = scr_path('objects_{0}.structjson')
        zlib_fname = scr_path('objects_{0}.inv')

        for fn in os.listdir(res_path()):
            # Drop unless testall
            if (not os.environ.get(TESTALL, False) and
                    fn != 'objects_attrs.inv'):
                continue
            
            # Only .inv
            if not fn.endswith('.inv'):
                continue

            proj = re.match('^objects_(.+?)\\.inv$', fn).group(1)
            sfx_fmt = '{0}_{1}'

            run_cmdline_test(self,
                             ['convert', 'plain',
                              src_fname.format(proj),
                              plain_fname.format(proj),
                              ],
                             suffix=sfx_fmt.format(proj, 'plain'))

            run_cmdline_test(self,
                             ['convert', 'json',
                              plain_fname.format(proj),
                              json_fname.format(proj),
                              ],
                             suffix=sfx_fmt.format(proj, 'json'))

            run_cmdline_test(self,
                             ['convert', 'struct',
                              json_fname.format(proj),
                              struct_fname.format(proj),
                              ],
                             suffix=sfx_fmt.format(proj, 'struct'))
            # Resume implementing conversion cycle


class inactiveGoodTests(object):

    def test_CmdlineDecompDiffSrcPathNewNameThere(self):
        """Confirm decomp in other path outputs there if only name passed."""
        copy_cmp()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        run_cmdline_test(self, ['decomp', scr_path(), dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        decomp_cmp_test(self, scr_path(dest_fname))

    def test_CmdlineCompressDiffSrcPathNewNameThere(self):
        """Confirm compress in other path outputs there if only name passed."""
        copy_dec()
        dest_fname = MOD_FNAME_BASE + CMP_EXT
        run_cmdline_test(self, ['comp', scr_path(), dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        sphinx_load_test(self, scr_path(dest_fname))

    def test_CmdlineDecompressDiffSrcTgtPaths(self):
        """Confirm decompress from other path to new path."""
        copy_cmp()
        dest_path = osp.join(os.curdir, MOD_FNAME_BASE + DEC_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['decomp', os.pardir, dest_path])

                        file_exists_test(self, dest_path)

                        decomp_cmp_test(self, dest_path)

    def test_CmdlineCompressDiffSrcTgtPaths(self):
        """Confirm compress from other path to new path."""
        copy_dec()
        dest_path = osp.join(os.curdir, MOD_FNAME_BASE + CMP_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['comp', os.pardir, dest_path])

                        file_exists_test(self, dest_path)

                        sphinx_load_test(self, dest_path)

    def test_CmdlineDecompressTgtBarePath(self):
        """Confirm decompress to target as bare path."""
        copy_cmp()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['decomp', os.pardir, '.'])

                        file_exists_test(self, INIT_FNAME_BASE + DEC_EXT)

                        decomp_cmp_test(self, INIT_FNAME_BASE + DEC_EXT)

    def test_CmdlineCompressTgtBarePath(self):
        """Confirm compress to target as bare path."""
        copy_dec()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['comp', os.pardir, '.'])

                        file_exists_test(self, INIT_FNAME_BASE + CMP_EXT)

                        sphinx_load_test(self, INIT_FNAME_BASE + CMP_EXT)


class TestSphobjinvCmdlineExpectFail(SuperSphobjinv, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    def test_CmdlinePlaintextNoArgs(self):
        """Confirm commandline plaintext convert w/no args fails."""
        copy_cmp()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['convert', 'plain'], expect=2)

    def test_CmdlinePlaintextWrongFileType(self):
        """Confirm exit code 1 with invalid file format."""
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    fname = 'testfile'
                    with open(fname, 'wb') as f:
                        f.write(b'this is not objects.inv\n')

                    run_cmdline_test(self,
                                     ['convert', 'plain', fname],
                                     expect=1)

    def test_CmdlinePlaintextMissingFile(self):
        """Confirm exit code 1 with nonexistent file specified."""
        run_cmdline_test(self, ['convert', 'plain', 'thisfileshouldbeabsent.txt'],
                         expect=1)

    def test_CmdlinePlaintextBadOutputFilename(self):
        """Confirm exit code 1 with invalid output file name."""
        copy_cmp()
        run_cmdline_test(self,
                         ['convert', 'plain',
                          scr_path(INIT_FNAME_BASE + CMP_EXT),
                          INVALID_FNAME],
                         expect=1)

    def test_CmdlineZlibNoArgs(self):
        """Confirm commandline zlib convert with no args fails."""
        copy_dec()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['convert', 'zlib'], expect=2)

    def test_CmdlinePlaintextSrcPathOnly(self):
        """Confirm cmdline plaintest convert with input directory arg fails."""
        copy_cmp()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain', scr_path()], expect=1)


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
