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

from .sphobjinv_base import DEC_EXT, CMP_EXT, JSON_EXT
from .sphobjinv_base import INIT_FNAME_BASE, MOD_FNAME_BASE
from .sphobjinv_base import RES_FNAME_BASE
from .sphobjinv_base import INVALID_FNAME, TESTALL
from .sphobjinv_base import SuperSphobjinv
from .sphobjinv_base import copy_dec, copy_cmp, scr_path, res_path
from .sphobjinv_base import copy_json
from .sphobjinv_base import decomp_cmp_test, file_exists_test
from .sphobjinv_base import run_cmdline_test, sphinx_load_test
from .sphobjinv_base import dir_change, stdio_mgr
from .sphobjinv_base import cmdline_sarge, run_cmdline_sarge


SARGE_WAIT = 5.0


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

    def test_CmdlineZlibToJSONSrcFileOnly(self):
        """Confirm cmdline JSON convert of zlib with input file arg."""
        copy_cmp()
        dest_path = scr_path(INIT_FNAME_BASE + JSON_EXT)
        run_cmdline_test(self, ['convert', 'json',
                                scr_path(INIT_FNAME_BASE + CMP_EXT)])

        file_exists_test(self, dest_path)

    def test_CmdlineJSONToPlaintextSrcFileOnly(self):
        """Confirm cmdline convert of flat JSON with input file arg."""
        copy_json()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + JSON_EXT)])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    def test_CmdlineJSONToZlibSrcFileOnly(self):
        """Confirm cmdline convert of JSON to zlib with input file arg."""
        copy_json()
        dest_path = scr_path(INIT_FNAME_BASE + CMP_EXT)
        run_cmdline_test(self, ['convert', 'zlib',
                                scr_path(INIT_FNAME_BASE + JSON_EXT)])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    def test_CmdlinePlaintextToZlibSrcFileOnly(self):
        """Confirm cmdline convert of plaintext to zlib with input file arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + CMP_EXT)
        run_cmdline_test(self, ['convert', 'zlib',
                                scr_path(INIT_FNAME_BASE + DEC_EXT)])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    def test_CmdlinePlaintextToJSONSrcFileOnly(self):
        """Confirm cmdline convert of plaintext to JSON with input file arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + JSON_EXT)
        run_cmdline_test(self, ['convert', 'json',
                                scr_path(INIT_FNAME_BASE + DEC_EXT)])

        file_exists_test(self, dest_path)

    def test_CmdlinePlaintextTgtNewName(self):
        """Confirm plaintext convert to custom target name in same dir."""
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

    def test_CmdlineDecompDiffSrcPathNewNameThere(self):
        """Confirm decomp in other path outputs there if only name passed."""
        copy_cmp()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + CMP_EXT),
                                dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        decomp_cmp_test(self, scr_path(dest_fname))

    def test_CmdlineDecompressDiffSrcTgtPaths(self):
        """Confirm decompress from other path to new path."""
        copy_cmp()
        dest_path = osp.join(os.curdir, MOD_FNAME_BASE + DEC_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['convert', 'plain',
                                          osp.join(os.pardir,
                                                   INIT_FNAME_BASE + CMP_EXT),
                                          dest_path])

                        file_exists_test(self, dest_path)

                        decomp_cmp_test(self, dest_path)

    def test_CmdlineDecompressTgtBarePath(self):
        """Confirm decompress to target as bare path (no filename)."""
        copy_cmp()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['convert', 'plain',
                                          osp.join(os.pardir,
                                                   INIT_FNAME_BASE + CMP_EXT),
                                          '.'])

                        file_exists_test(self, INIT_FNAME_BASE + DEC_EXT)

                        decomp_cmp_test(self, INIT_FNAME_BASE + DEC_EXT)

    def test_CmdlineCycleConvert(self):
        """Confirm conversion in a loop, reading all formats."""
        from itertools import product
        import json
        import re

        from sphobjinv import Inventory as Inv
        from sphobjinv import HeaderFields as HF

        src_fname = res_path('objects_{0}.inv')
        plain_fname = scr_path('objects_{0}.txt')
        json_fname = scr_path('objects_{0}.json')
        zlib_fname = scr_path('objects_{0}.inv')

        sfx_fmt = '{0}_{1}'

        for fn in os.listdir(res_path()):
            # Drop unless testall
            if (not os.environ.get(TESTALL, False) and
                    fn != 'objects_attrs.inv'):
                continue

            # Only .inv
            if not fn.endswith('.inv'):
                continue

            proj = re.match('^objects_(.+?)\\.inv$', fn).group(1)

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
                             ['convert', 'zlib',
                              json_fname.format(proj),
                              zlib_fname.format(proj),
                              ],
                             suffix=sfx_fmt.format(proj, 'zlib'))

            # Reimport all and check header info
            invs = {}
            invs.update({'orig': Inv(src_fname.format(proj))})
            invs.update({'plain': Inv(plain_fname.format(proj))})
            invs.update({'zlib': Inv(zlib_fname.format(proj))})
            with open(json_fname.format(proj)) as f:
                invs.update({'json': Inv(json.load(f))})

            for t, a in product(('plain', 'zlib', 'json'),
                                (HF.Project.value, HF.Version.value,
                                 HF.Count.value)):
                with self.subTest(sfx_fmt.format(t, a)):
                        self.assertEqual(getattr(invs[t], a),
                                         getattr(invs['orig'], a))

    def test_Cmdline_OverwritePromptAndBehavior(self):
        """Confirm overwrite prompt works properly."""
        from sphobjinv import Inventory as Inv

        src1 = res_path('objects_attrs.inv')
        src2 = res_path('objects_sarge.inv')
        dst = scr_path(INIT_FNAME_BASE + DEC_EXT)
        args = ['convert', 'plain', src1, dst]

        # Initial decompress
        run_cmdline_sarge(self, args)

        # First overwrite, declining clobber
        args[2] = src2
        with cmdline_sarge(args) as (pipe, feed):
            mch = pipe.stdout.expect('(Y/N)? ', timeout=SARGE_WAIT)

            if mch is None:
                self.fail('First, declined overwrite timed out')

            feed.feed('N\n')
            mch = pipe.stdout.expect('Exiting', timeout=SARGE_WAIT)

        with self.subTest('no_clobber'):
            self.assertEqual('attrs', Inv(dst).project)

        # Second overwrite, with clobber
        with cmdline_sarge(args) as (pipe, feed):
            mch = pipe.stdout.expect('(Y/N)? ', timeout=SARGE_WAIT)

            if mch is None:
                self.fail('Second, confirmed overwrite timed out @ start')

            feed.feed('Y\n')
            mch = pipe.stdout.expect('(plain)', timeout=SARGE_WAIT)

            if mch is None:
                self.fail('Second, confirmed overwrite timed out @ write')

        with self.subTest('clobber'):
            self.assertEqual('Sarge', Inv(dst).project)

    def test_Cmdline_SuggestCleanExit(self):
        """Confirm suggest clean exit, no output check.

        For coverage.

        """
        with self.subTest('just_names'):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'validate',
                                    '-t', '50'])

        with self.subTest('with_score'):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'validate',
                                    '-st', '50'])

        with self.subTest('with_index'):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'validate',
                                    '-it', '50'])

        with self.subTest('with_both'):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'validate',
                                    '-sit', '50'])


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
        run_cmdline_test(self, ['convert', 'plain',
                                'thisfileshouldbeabsent.txt'],
                         expect=1)

    def test_CmdlinePlaintextBadOutputFilename(self):
        """Confirm exit code 1 with invalid output file name."""
        copy_cmp()
        run_cmdline_test(self,
                         ['convert', 'plain',
                          scr_path(INIT_FNAME_BASE + CMP_EXT),
                          INVALID_FNAME],
                         expect=1)

    def test_Cmdline_BadOutputDir(self):
        """Confirm exit code 1 when output location can't be created."""
        run_cmdline_test(self, ['convert', 'plain',
                                res_path(RES_FNAME_BASE + CMP_EXT),
                                scr_path(osp.join('nonexistent', 'folder',
                                                  'obj.txt'))],
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
