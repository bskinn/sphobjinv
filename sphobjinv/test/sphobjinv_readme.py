# ------------------------------------------------------------------------------
# Name:        sphobjinv_readme
# Purpose:     Module for sphobjinv README doctests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     6 Aug 2018
# Copyright:   (c) Brian Skinn 2016-2018
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Module for sphobjinv API tests."""

import doctest as dt
import os.path as osp
import re
import shlex
import subprocess as sp
import sys
from textwrap import dedent
import unittest as ut


p_shell = re.compile("""
    \\n\\s+[$](?P<cmd>.*)        # Entered command
    (?P<out>(\\n\\s+.*)+?)       # Line(s) of output
    (?=(\\n\\n|\\n\\s+[$]))      # Lookahead for end of output
    """, re.X)


py_ver = sys.version_info


@ut.skipUnless(py_ver[0] > 3 or (py_ver[0] == 3 and py_ver[1] >= 5),
               "Skip on Python 3.4 due to variant subprocess behavior")
class TestReadmeShellCmds(ut.TestCase):
    """Testing README shell command output."""

    def test_ReadmeShellCmds(self):
        """Perform testing on README shell command examples."""
        self.maxDiff = None

        with open('README.rst') as f:
            text = f.read()

        chk = dt.OutputChecker()

        cmds = [_.group('cmd') for _ in p_shell.finditer(text)]
        outs = [dedent(_.group('out')) for _ in p_shell.finditer(text)]

        for i, tup in enumerate(zip(cmds, outs)):
            c, o = tup

            with self.subTest('exec_{0}'.format(i)):
                proc = sp.run(shlex.split(c), stdout=sp.PIPE,
                              stderr=sp.STDOUT, timeout=30,
                              )

            result = proc.stdout.decode('utf-8')
            dt_flags = dt.ELLIPSIS | dt.NORMALIZE_WHITESPACE

            with self.subTest('check_{0}'.format(i)):
                self.assertTrue(chk.check_output(o, result, dt_flags),
                                msg='\n'.join((o, result)))


def setup_soi_import(dt_obj):
    """Import sphobjinv into test globals."""
    import sphobjinv as soi
    dt_obj.globs.update({'soi': soi})


# Handles REPL tests
TestReadme = dt.DocFileSuite(osp.abspath('README.rst'),
                             module_relative=False,
                             setUp=setup_soi_import,
                             optionflags=dt.ELLIPSIS,
                             )


def suite_doctest_readme():
    """Create and return the test suite for README."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestReadmeShellCmds),
                TestReadme,
                ])

    return s


if __name__ == '__main__':
    print("Module not executable.")
