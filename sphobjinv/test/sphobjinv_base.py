# ------------------------------------------------------------------------------
# Name:        sphobjinv_base
# Purpose:     Module defining common objects for sphobjinv tests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     29 Oct 2017
# Copyright:   (c) Brian Skinn 2016-2018
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Module defining common objects for sphobjinv tests."""


from contextlib import contextmanager
from filecmp import cmp
from io import StringIO, TextIOBase
import os
import os.path as osp
import re
import shutil as sh
import sys

import attr


# Useful constants
RES_FNAME_BASE = 'objects_attrs'
INIT_FNAME_BASE = 'objects'
MOD_FNAME_BASE = 'objects_mod'

CMP_EXT = '.inv'
DEC_EXT = '.txt'
JSON_EXT = '.json'

SOI_PATH = osp.abspath(osp.join('sphobjinv', 'sphobjinv.py'))
INVALID_FNAME = '*?*?.txt' if os.name == 'nt' else '/'
B_LINES_0 = {False:
             b'attr.Attribute py:class 1 api.html#$ -',
             True:
             b'attr.Attribute py:class 1 api.html#attr.Attribute '
             b'attr.Attribute'}
S_LINES_0 = {_: B_LINES_0[_].decode('utf-8') for _ in B_LINES_0}

# Constant mainly for the many-inventory URL testing
REMOTE_URL = ('https://github.com/bskinn/sphobjinv/raw/dev/sphobjinv/'
              'test/resource/objects_{0}.inv')


# Regex pattern for objects.inv files
P_INV = re.compile('objects_([\\w\\d]+)\\.inv', re.I)


# Environ flag for testing all or not
TESTALL = 'TESTALL'


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
    if osp.isdir(scr_path()):
        sh.rmtree(scr_path())


def copy_cmp():
    """Copy the compressed example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + CMP_EXT),
            scr_path(INIT_FNAME_BASE + CMP_EXT))


def copy_dec():
    """Copy the decompressed example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + DEC_EXT),
            scr_path(INIT_FNAME_BASE + DEC_EXT))


def copy_json():
    """Copy the JSON example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + JSON_EXT),
            scr_path(INIT_FNAME_BASE + JSON_EXT))


def sphinx_load_test(testcase, path):
    """Perform 'live' Sphinx inventory load test."""
    # Easier to have the file open the whole time
    with open(path, 'rb') as f:

        from sphinx.util.inventory import InventoryFile as IFile

        # Attempt the load operation
        try:
            IFile.load(f, '', osp.join)
        except Exception:
            with testcase.subTest('sphinx_load_ok'):
                testcase.fail()


def run_cmdline_test(testcase, arglist, *, expect=0, suffix=None):
    """Perform command line test."""
    from sphobjinv.cmdline import main

    # Assemble execution arguments
    runargs = ['sphobjinv']
    runargs.extend(arglist)

    # Mock sys.argv, run main, and restore sys.argv
    stored_sys_argv = sys.argv
    sys.argv = runargs
    try:
        main()
    except SystemExit as e:
        retcode = e.args[0]
    else:
        raise RuntimeError("SystemExit not raised on termination.")
    finally:
        sys.argv = stored_sys_argv

    # Test that execution completed w/indicated exit code
    with testcase.subTest('exit_code' + ('_' + suffix if suffix else '')):
        testcase.assertEqual(expect, retcode)


def file_exists_test(testcase, path, suffix=None):
    """Confirm indicated filespec exists."""
    with testcase.subTest('file_exists' + ('_' + suffix if suffix else '')):
        testcase.assertTrue(osp.isfile(path))


def decomp_cmp_test(testcase, path):
    """Confirm that indicated decompressed file is identical to resource."""
    with testcase.subTest('decomp_cmp'):
        testcase.assertTrue(cmp(RES_DECOMP_PATH, path, shallow=False))


@contextmanager
def dir_change(subdir):
    """Context manager to change to sub-directory & drop back on exit."""
    from time import sleep

    existed = osp.isdir(subdir)

    if not existed:
        os.mkdir(subdir)

    os.chdir(subdir)
    yield

    # Wait briefly to ensure yielded-to operations are fully complete
    sleep(0.02)

    if not existed:
        list(map(os.remove, os.listdir()))

    os.chdir(os.pardir)

    if not existed:
        os.rmdir(subdir)


@attr.s(slots=True)
class TeeStdin(StringIO):
    """Class to tee contents to a side buffer on read.

    Also provides .append(), which adds new content to the end of the
    stream while leaving the read position unchanged.

    """

    from io import SEEK_SET, SEEK_END

    tee = attr.ib(validator=attr.validators.instance_of(TextIOBase))
    init_text = attr.ib(default='',
                        validator=attr.validators.instance_of(str))

    def __attrs_post_init__(self):
        """Call normal __init__ on superclass."""
        super().__init__(self.init_text)

    def read(self, size=None):
        """Tee text to side buffer when read."""
        text = super().read(size)
        self.tee.write(text)
        return text

    def readline(self, size=-1):
        """Tee text to side buffer when read."""
        text = super().readline(size)
        self.tee.write(text)
        return text

    def append(self, text):
        """Write to end of stream, restore position."""
        pos = self.tell()
        self.seek(0, self.SEEK_END)
        retval = self.write(text)
        self.seek(pos, self.SEEK_SET)
        return retval


@contextmanager
def stdio_mgr(sys, cmd_str=''):
    """Prepare sys for custom I/O."""
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    new_stdout = StringIO()
    new_stderr = StringIO()
    new_stdin = TeeStdin(new_stdout, cmd_str)

    sys.stdin = new_stdin
    sys.stdout = new_stdout
    sys.stderr = new_stderr

    yield new_stdin, new_stdout, new_stderr

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    sys.stdout.write(new_stdout.read())
    sys.stderr.write(new_stderr.read())

    new_stdin.close()
    new_stdout.close()
    new_stderr.close()


class SuperSphobjinv(object):
    """Superclass with common setup/teardown code for all tests."""

    def setUp(self):
        """Run the per-test-method setup code."""
        # Ensure the scratch
        ensure_scratch()

    def tearDown(self):
        """Run the per-test tear-down code."""
        # Remove the scratch
        clear_scratch()


if __name__ == '__main__':
    print("Module not executable.")
