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
import os
import os.path as osp
import re
import shutil as sh
import sys


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
def cmdline_sarge(cmdlist):
    """Bootstrap a sarge-governed cmdline exec."""
    import sarge

    arglist = ['python', '-m', 'sphobjinv.cmdline']
    arglist.extend(cmdlist)

    feeder = sarge.Feeder()
    pipeline = sarge.run(arglist, async=True, input=feeder,
                         stdout=sarge.Capture(buffer_size=1),
                         stderr=sarge.Capture(buffer_size=1))

    yield pipeline, feeder

    if pipeline.commands[0].poll() is None:
        pipeline.commands[0].terminate()


def run_cmdline_sarge(testcase, arglist, *, expect=0, suffix=None,
                      poll_intv=0.2, timeout=5.0):
    """Perform command line test with sarge.

    Can only be executed when cwd is the repo root, otherwise
    sphobjinv is not on the package search path.

    """
    import time

    with cmdline_sarge(arglist) as (pipe, feed):
        start_time = time.time()

        while pipe.commands[0].poll() is None:
            time.sleep(poll_intv)
            if time.time() - start_time > timeout:
                testcase.fail('Execution timed out')

    # Test that execution completed w/indicated exit code
    with testcase.subTest('exit_code' + ('_' + suffix if suffix else '')):
        testcase.assertEqual(expect, pipe.commands[0].returncode)

    return pipe


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
