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


CLI_TIMEOUT = 2.0


class TestSphobjinvCmdlineExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    @timeout(CLI_TIMEOUT)
    def test_CmdlineZlibToPlaintextSrcFileOnly(self):
        """Confirm cmdline decompress of zlib with input file arg."""
        copy_cmp()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + CMP_EXT)])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    @timeout(CLI_TIMEOUT)
    def test_CmdlineZlibToPlaintextSrcFileOnlyExpandContract(self):
        """Confirm cmdline contract decompress of zlib with input file arg."""
        copy_cmp()

        cmp_path = scr_path(INIT_FNAME_BASE + CMP_EXT)
        dec_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        recmp_path = scr_path(MOD_FNAME_BASE + CMP_EXT)

        run_cmdline_test(self, ['convert', 'plain', '-e', cmp_path])
        file_exists_test(self, dec_path)

        run_cmdline_test(self, ['convert', 'zlib', '-c',
                                dec_path, recmp_path])
        file_exists_test(self, recmp_path)

    @timeout(CLI_TIMEOUT)
    def test_CmdlineZlibToJSONSrcFileOnly(self):
        """Confirm cmdline JSON convert of zlib with input file arg."""
        copy_cmp()
        dest_path = scr_path(INIT_FNAME_BASE + JSON_EXT)
        run_cmdline_test(self, ['convert', 'json',
                                scr_path(INIT_FNAME_BASE + CMP_EXT)])

        file_exists_test(self, dest_path)

    @timeout(CLI_TIMEOUT)
    def test_CmdlineJSONToPlaintextSrcFileOnly(self):
        """Confirm cmdline convert of flat JSON with input file arg."""
        copy_json()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + JSON_EXT)])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    @timeout(CLI_TIMEOUT)
    def test_CmdlineJSONToZlibSrcFileOnly(self):
        """Confirm cmdline convert of JSON to zlib with input file arg."""
        copy_json()
        dest_path = scr_path(INIT_FNAME_BASE + CMP_EXT)
        run_cmdline_test(self, ['convert', 'zlib',
                                scr_path(INIT_FNAME_BASE + JSON_EXT)])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    @timeout(CLI_TIMEOUT)
    def test_CmdlinePlaintextToZlibSrcFileOnly(self):
        """Confirm cmdline convert of plaintext to zlib with input file arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + CMP_EXT)
        run_cmdline_test(self, ['convert', 'zlib',
                                scr_path(INIT_FNAME_BASE + DEC_EXT)])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    @timeout(CLI_TIMEOUT)
    def test_CmdlinePlaintextToJSONSrcFileOnly(self):
        """Confirm cmdline convert of plaintext to JSON with input file arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + JSON_EXT)
        run_cmdline_test(self, ['convert', 'json',
                                scr_path(INIT_FNAME_BASE + DEC_EXT)])

        file_exists_test(self, dest_path)

    @timeout(CLI_TIMEOUT)
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

    @timeout(CLI_TIMEOUT)
    def test_CmdlineDecompDiffSrcPathNewNameThere(self):
        """Confirm decomp in other path outputs there if only name passed."""
        copy_cmp()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        run_cmdline_test(self, ['convert', 'plain',
                                scr_path(INIT_FNAME_BASE + CMP_EXT),
                                dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        decomp_cmp_test(self, scr_path(dest_fname))

    @timeout(CLI_TIMEOUT)
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

    @timeout(CLI_TIMEOUT)
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

    @timeout(CLI_TIMEOUT * 52 * 3)
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

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_OverwritePromptAndBehavior(self):
        """Confirm overwrite prompt works properly."""
        from sphobjinv import Inventory as Inv

        src1 = res_path('objects_attrs.inv')
        src2 = res_path('objects_sarge.inv')
        dst = scr_path(INIT_FNAME_BASE + DEC_EXT)
        args = ['convert', 'plain', src1, dst]

        # Initial decompress
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, args, suffix='initial')

            with self.subTest('initial_stdout'):
                self.assertIn('converted', out_.getvalue())
                self.assertIn('(plain)', out_.getvalue())

        # First overwrite, declining clobber
        args[2] = src2
        with stdio_mgr() as (in_, out_, err_):
            in_.append('n\n')
            run_cmdline_test(self, args, suffix='no_overwrite')

            with self.subTest('no_overwrite_stdout'):
                self.assertIn('(Y/N)? n', out_.getvalue())

        with self.subTest('no_overwrite_project'):
            self.assertEqual('attrs', Inv(dst).project)

        # Second overwrite, with clobber
        with stdio_mgr() as (in_, out_, err_):
            in_.append('y\n')
            run_cmdline_test(self, args, suffix='overwrite')

            with self.subTest('overwrite_stdout'):
                self.assertIn('(Y/N)? y', out_.getvalue())

        with self.subTest('overwrite_project'):
            self.assertEqual('Sarge', Inv(dst).project)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_SuggestNoResults(self):
        """Confirm suggest w/no found results works."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-t', '99'])

            with self.subTest('nothing_found_msg'):
                self.assertIn('No results found.', out_.getvalue())

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_SuggestNameOnly(self):
        """Confirm name-only suggest works."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-t', '50'])

            p = re.compile('^.*instance_of.*$', re.M)

            with self.subTest('found_object'):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_SuggestWithIndex(self):
        """Confirm with_index suggest works."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-it', '50'])

            p = re.compile('^.*instance_of\\S*\\s+23\\s*$', re.M)

            with self.subTest('found_object'):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_SuggestWithScore(self):
        """Confirm with_index suggest works."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-st', '50'])

            p = re.compile('^.*instance_of\\S*\\s+\\d+\\s*$', re.M)

            with self.subTest('found_object'):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_SuggestWithScoreAndIndex(self):
        """Confirm with_index suggest works."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-sit', '50'])

            p = re.compile('^.*instance_of\\S*\\s+\\d+\\s+23\\s*$', re.M)

            with self.subTest('found_object'):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_SuggestLongListLinesCount(self):
        """Confirm with_index suggest works."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-at', '1'],
                             suffix='all_arg')

            with self.subTest('count_all_arg'):
                self.assertEqual(out_.getvalue().count('\n'), 56)

        with stdio_mgr() as (in_, out_, err_):
            in_.append('y\n')
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-t', '1'],
                             suffix='no_arg')

            with self.subTest('count_no_arg'):
                # Extra newline due to input() query
                self.assertEqual(out_.getvalue().count('\n'), 57)

        with stdio_mgr() as (in_, out_, err_):
            in_.append('n\n')
            run_cmdline_test(self, ['suggest',
                                    res_path(RES_FNAME_BASE + CMP_EXT),
                                    'instance',
                                    '-t', '1'],
                             suffix='no_print')

            with self.subTest('count_no_print'):
                self.assertEqual(out_.getvalue().count('\n'), 3)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_VersionExitsOK(self):
        """Confirm --version exits cleanly."""
        run_cmdline_test(self, ['-v'])

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_NoArgsShowsHelp(self):
        """Confirm help shown when invoked with no arguments."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, [])

            with self.subTest('help_displayed'):
                self.assertIn('usage: sphobjinv', out_.getvalue())


class TestSphobjinvCmdlineExpectGoodNonlocal(SuperSphobjinv, ut.TestCase):
    """Testing nonlocal code expecting to work properly."""

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_SuggestNameOnlyFromURL(self):
        """Confirm name-only suggest works from URL."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['suggest', '-u',
                                    REMOTE_URL.format('attrs'),
                                    'instance',
                                    '-t', '50'])

            p = re.compile('^.*instance_of.*$', re.M)

            with self.subTest('found_object'):
                self.assertRegex(out_.getvalue(), p)

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_ConvertURLToPlaintextOutfileProvided(self):
        """Confirm CLI URL D/L, convert works w/outfile supplied."""
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['convert', 'plain', '-u',
                                REMOTE_URL.format('attrs'),
                                dest_path])

        file_exists_test(self, dest_path)

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_ConvertURLToPlaintextNoOutfile(self):
        """Confirm CLI URL D/L, convert works w/o outfile supplied."""
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['convert', 'plain', '-u',
                                            REMOTE_URL.format('attrs')])

        file_exists_test(self, dest_path)


class TestSphobjinvCmdlineExpectFail(SuperSphobjinv, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    @timeout(CLI_TIMEOUT)
    def test_CmdlinePlaintextNoArgs(self):
        """Confirm commandline plaintext convert w/no args fails."""
        copy_cmp()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['convert', 'plain'], expect=2)

    @timeout(CLI_TIMEOUT)
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

    @timeout(CLI_TIMEOUT)
    def test_CmdlinePlaintextMissingFile(self):
        """Confirm exit code 1 with nonexistent file specified."""
        run_cmdline_test(self, ['convert', 'plain',
                                'thisfileshouldbeabsent.txt'],
                         expect=1)

    @timeout(CLI_TIMEOUT)
    def test_CmdlinePlaintextBadOutputFilename(self):
        """Confirm exit code 1 with invalid output file name."""
        copy_cmp()
        run_cmdline_test(self,
                         ['convert', 'plain',
                          scr_path(INIT_FNAME_BASE + CMP_EXT),
                          INVALID_FNAME],
                         expect=1)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_BadOutputDir(self):
        """Confirm exit code 1 when output location can't be created."""
        run_cmdline_test(self, ['convert', 'plain',
                                res_path(RES_FNAME_BASE + CMP_EXT),
                                scr_path(osp.join('nonexistent', 'folder',
                                                  'obj.txt'))],
                         expect=1)

    @timeout(CLI_TIMEOUT)
    def test_CmdlineZlibNoArgs(self):
        """Confirm commandline zlib convert with no args fails."""
        copy_dec()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['convert', 'zlib'], expect=2)

    @timeout(CLI_TIMEOUT)
    def test_CmdlinePlaintextSrcPathOnly(self):
        """Confirm cmdline plaintest convert with input directory arg fails."""
        copy_cmp()
        run_cmdline_test(self, ['convert', 'plain', scr_path()], expect=1)

    @timeout(CLI_TIMEOUT)
    def test_Cmdline_AttemptURLOnLocalFile(self):
        """Confirm error when using URL mode on local file."""
        copy_cmp()
        in_path = scr_path(INIT_FNAME_BASE + CMP_EXT)

        run_cmdline_test(self, ['convert', 'plain', '-u', in_path],
                         expect=1)

        file_url = 'file:///' + os.path.abspath(in_path)
        run_cmdline_test(self, ['convert', 'plain', '-u', file_url],
                         expect=1)


class TestSphobjinvCmdlineExpectFailNonlocal(SuperSphobjinv, ut.TestCase):
    """Check expect-fail cases with non-local sources/effects."""

    @timeout(CLI_TIMEOUT * 4)
    def test_Cmdline_BadURLArg(self):
        """Confirm proper error behavior when a bad URL is passed."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(self, ['convert', 'plain', '-u',
                                    REMOTE_URL.format('blarghers'),
                                    scr_path()],
                             expect=1)

            with self.subTest('stdout_match'):
                self.assertIn('Error while downloading/parsing URL:',
                              out_.getvalue())


def suite_cli_expect_good():
    """Create and return the test suite for CLI expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvCmdlineExpectGood)])

    return s


def suite_cli_expect_good_nonlocal():
    """Create and return the test suite for nonlocal CLI expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(
        TestSphobjinvCmdlineExpectGoodNonlocal)])

    return s


def suite_cli_expect_fail():
    """Create and return the test suite for CLI expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvCmdlineExpectFail)])

    return s


def suite_cli_expect_fail_nonlocal():
    """Create and return the test suite for nonlocal CLI expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(
        TestSphobjinvCmdlineExpectFailNonlocal)])

    return s


if __name__ == '__main__':
    print("Module not executable.")
