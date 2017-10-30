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
# import sys
import unittest as ut


def res_path(fname):
    """Construct file path in resource dir from project root."""
    return osp.join('sphobjinv', 'test', 'resource', fname)


def scr_path(fname):
    """Construct file path in scratch dir from project root."""
    return osp.join('sphobjinv', 'test', 'scratch', fname)


class TestSphobjinvExpectGood(ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_DummyPass(self):
        """Perform dummy test."""
        self.assertIn('objects_attrs.inv', os.listdir(res_path('')))


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
