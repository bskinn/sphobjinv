# ------------------------------------------------------------------------------
# Name:        sphobjinv_base
# Purpose:     Base module for sphobjinv tests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     29 Oct 2017
# Copyright:   (c) Brian Skinn 2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Base module for sphobjinv tests."""


# import doctest as dt
import os
import os.path as osp
import shutil as sh
# import sys
import unittest as ut


# Useful constants
RES_FNAME_BASE = 'objects_attrs'
INIT_FNAME_BASE = 'objects'
MOD_FNAME_BASE = 'objects_mod'
ENC_EXT = '.inv'
DEC_EXT = '.txt'


# Useful functions
def res_path(fname=''):
    """Construct file path in resource dir from project root."""
    return osp.join('sphobjinv', 'test', 'resource', fname)


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
        os.remove(scr_path(fn))


def copy_enc():
    """Copy the encoded example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + ENC_EXT),
            scr_path(INIT_FNAME_BASE + ENC_EXT))


def copy_dec():
    """Copy the decoded example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + DEC_EXT),
            scr_path(INIT_FNAME_BASE + DEC_EXT))


def sphinx_inv_test(testcase, path):
    """Perform 'live' Sphinx inventory load test."""
    from sphinx.util.inventory import InventoryFile as IFile
    try:
        with open(path, 'rb') as f:
            IFile.load(f, 'C:\\', osp.join)
    except Exception:
        testcase.fail()


class TestSphobjinvExpectGood(ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    @classmethod
    def setUpClass(cls):
        """Run the class-wide setup code."""
        ensure_scratch()

    def test_APIEncodeSucceeds(self):
        """Check that an encode attempt via API throws no errors."""
        import sphobjinv as soi

        clear_scratch()
        copy_dec()

        # See if it makes it all the way through the process without error
        with self.subTest('error_in_process'):
            try:
                b_dec = soi.readfile(scr_path(INIT_FNAME_BASE + DEC_EXT))
                b_enc = soi.encode(b_dec)
                soi.writefile(scr_path(MOD_FNAME_BASE + ENC_EXT), b_enc)
            except Exception:
                self.fail(msg='objects.txt encoding failed.')

        # Simple assertion that encoded file now exists
        with self.subTest('file_exists'):
            self.assertTrue(osp.isfile(scr_path(MOD_FNAME_BASE + ENC_EXT)))

        # Seeing if intersphinx actually likes the file
        with self.subTest('intersphinx_is_ok'):
            sphinx_inv_test(self, scr_path(MOD_FNAME_BASE + ENC_EXT))

    def test_APIDecodeSucceeds(self):
        """Check that a decode attempt via API throws no errors."""
        import sphobjinv as soi

        clear_scratch()
        copy_enc()

        # See if the encode operation completes without error
        with self.subTest('error_in_process'):
            try:
                b_enc = soi.readfile(scr_path(INIT_FNAME_BASE + ENC_EXT))
                b_dec = soi.decode(b_enc)
                soi.writefile(scr_path(MOD_FNAME_BASE + DEC_EXT), b_dec)
            except Exception:
                self.fail(msg='objects.inv decoding failed.')

        # Simple assertion of the existence of the decoded file
        with self.subTest('file_exists'):
            self.assertTrue(osp.isfile(scr_path(MOD_FNAME_BASE + DEC_EXT)))


class TestSphobjinvExpectFail(ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    def test_DummyPass(self):
        """Perform dummy test."""
        self.assertTrue(True)


# Doctest suite for testing README.rst example code
# SuiteDoctestReadme = dt.DocFileSuite('README.rst',
#                                      module_relative=False)


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
