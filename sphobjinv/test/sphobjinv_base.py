# ------------------------------------------------------------------------------
# Name:        sphobjinv_base
# Purpose:     Base module for sphobjinv tests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     29 Oct 2017
# Copyright:   (c) Brian Skinn 2016-2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Base module for sphobjinv tests."""


from contextlib import contextmanager
from filecmp import cmp
import os
import os.path as osp
import shutil as sh
import subprocess as sp
import sys
import unittest as ut


# Useful constants
RES_FNAME_BASE = 'objects_attrs'
INIT_FNAME_BASE = 'objects'
MOD_FNAME_BASE = 'objects_mod'
ENC_EXT = '.inv'
DEC_EXT = '.txt'
SOI_PATH = osp.abspath(osp.join('sphobjinv', 'sphobjinv.py'))


# Useful functions
def res_path(fname=''):
    """Construct file path in resource dir from project root."""
    return osp.join('sphobjinv', 'test', 'resource', fname)


# Absolute path to the .txt file in `resource`
# This has to come after res_path is defined
RES_DECOMP_PATH = osp.abspath(res_path(RES_FNAME_BASE + DEC_EXT))


def scr_path(fname=''):
    """Construct file path in scratch dir from project root."""
    return osp.join('sphobjinv', 'test', 'scratch', fname)


def ensure_scratch():
    """Ensure the scratch folder exists."""
    if not osp.isdir(scr_path()):
        os.mkdir(scr_path())


def clear_scratch():
    """Clear the scratch folder."""
    for fn in os.listdir(scr_path()):
        if osp.isfile(scr_path(fn)):
            os.remove(scr_path(fn))


def copy_enc():
    """Copy the encoded example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + ENC_EXT),
            scr_path(INIT_FNAME_BASE + ENC_EXT))


def copy_dec():
    """Copy the decoded example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + DEC_EXT),
            scr_path(INIT_FNAME_BASE + DEC_EXT))


def sphinx_load_test(testcase, path):
    """Perform 'live' Sphinx inventory load test."""
    # Easier to have the file open the whole time
    with open(path, 'rb') as f:

        # Have to handle it differently for Python 3.3 compared to the rest
        if sys.version_info.major == 3 and sys.version_info.minor < 4:
            from sphinx.ext.intersphinx import read_inventory_v2 as readfunc
            f.readline()    # read_inventory_v2 expects to start on 2nd line
        else:
            from sphinx.util.inventory import InventoryFile as IFile
            readfunc = IFile.load

        # Attempt the load operation
        try:
            readfunc(f, '', osp.join)
        except Exception:
            with testcase.subTest('sphinx_load_ok'):
                testcase.fail()


def run_cmdline_test(testcase, arglist, expect=0):
    """Perform command line test."""
    # Assemble execution arguments
    runargs = ['python', SOI_PATH]
    list(map(runargs.append, arglist))

    # subprocess.run only available on Python 3.5+
    # Interested in the return code for now
    try:
        retcode = sp.run(runargs).returncode
    except AttributeError:
        retcode = sp.call(runargs)

    # Test that execution completed w/o error
    with testcase.subTest('exit_code'):
        testcase.assertEquals(expect, retcode)


def file_exists_test(testcase, path):
    """Confirm indicated filespec exists."""
    with testcase.subTest('file_exists'):
        testcase.assertTrue(osp.isfile(path))


def decomp_cmp_test(testcase, path):
    """Confirm that indicated decoded file compares identical to resource."""
    with testcase.subTest('decomp_cmp'):
        testcase.assertTrue(cmp(RES_DECOMP_PATH, path, shallow=False))


@contextmanager
def dir_change(subdir):
    """Context manager to change to sub-directory & drop back on exit."""
    existed = osp.isdir(subdir)

    if not existed:
        os.mkdir(subdir)

    os.chdir(subdir)
    yield

    if not existed:
        list(map(os.remove, os.listdir()))

    os.chdir(os.pardir)

    if not existed:
        os.rmdir(subdir)


class SuperSphobjinv(object):
    """Superclass with common setup code for all tests."""

    @classmethod
    def setUpClass(cls):
        """Run the class-wide setup code."""
        # Make sure the scratch directory exists.
        ensure_scratch()

    def setUp(self):
        """Run the per-test-method setup code."""
        # Always want to clear the scratch?
        clear_scratch()


class SubTestMasker(object):
    """Inheritance class to implement mocked version of .subTest."""

    if sys.version_info.major == 3 and sys.version_info.minor < 4:
        @contextmanager
        def subTest(testcase, name):
            """Mock TestCase.subTest for Python versions <3.4."""
            yield


class TestSphobjinvExpectGood(SuperSphobjinv, ut.TestCase, SubTestMasker):
    """Testing code accuracy under good params & expected behavior."""

    def test_APIEncodeSucceeds(self):
        """Check that an encode attempt via API throws no errors."""
        import sphobjinv as soi

        # Populate scratch with the decoded ref file
        copy_dec()

        # Store dest filename for reuse
        dest_fname = scr_path(MOD_FNAME_BASE + ENC_EXT)

        # See if it makes it all the way through the process without error
        with self.subTest('error_in_process'):
            try:
                b_dec = soi.readfile(scr_path(INIT_FNAME_BASE + DEC_EXT))
                b_enc = soi.encode(b_dec)
                soi.writefile(dest_fname, b_enc)
            except Exception:
                self.fail(msg='objects.txt encoding failed.')

        # Simple assertion that encoded file now exists
        file_exists_test(self, dest_fname)

        # Seeing if sphinx actually likes the file
        sphinx_load_test(self, dest_fname)

    def test_APIDecodeSucceeds(self):
        """Check that a decode attempt via API throws no errors."""
        import sphobjinv as soi

        # Populate scratch with encoded ref file
        copy_enc()

        # Store target filename for reuse
        dest_fname = scr_path(MOD_FNAME_BASE + DEC_EXT)

        # See if the encode operation completes without error
        with self.subTest('error_in_process'):
            try:
                b_enc = soi.readfile(scr_path(INIT_FNAME_BASE + ENC_EXT))
                b_dec = soi.decode(b_enc)
                soi.writefile(dest_fname, b_dec)
            except Exception:
                self.fail(msg='objects.inv decoding failed.')

        # Simple assertion of the existence of the decoded file
        file_exists_test(self, dest_fname)

        # Testing compare w/original file
        decomp_cmp_test(self, dest_fname)

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


class TestSphobjinvExpectFail(SuperSphobjinv, ut.TestCase, SubTestMasker):
    """Testing that code raises expected errors when invoked improperly."""

    def test_APINoInputFile(self):
        """Confirm that appropriate exceptions are raised w/no input file."""
        import sphobjinv as soi

        with self.subTest('decoded_input_file'):
            with self.assertRaises(FileNotFoundError):
                soi.readfile(INIT_FNAME_BASE + DEC_EXT)

        with self.subTest('encoded_input_file'):
            with self.assertRaises(FileNotFoundError):
                soi.readfile(INIT_FNAME_BASE + ENC_EXT)

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


def suite_expect_good():
    """Create and return the test suite for expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvExpectGood)])
#               SuiteDoctestReadme])

    return s


def suite_expect_fail():
    """Create and return the test suite for expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvExpectFail)])

    return s


if __name__ == '__main__':  # pragma: no cover
    print("Module not executable.")
