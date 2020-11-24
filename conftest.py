r"""*Root conftest for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    20 Mar 2019

**Copyright**
    \(c) Brian Skinn 2016-2020

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""


import os.path as osp
import platform
import re
import shutil
import sys
from enum import Enum
from filecmp import cmp
from functools import partial
from pathlib import Path

import jsonschema
import pytest

import sphobjinv as soi


def pytest_addoption(parser):
    """Add custom CLI options to pytest."""
    parser.addoption(
        "--testall",
        action="store_true",
        help=(
            "Where relevant, test *all* inventories stored in "
            "testing resource folder, not just objects_attrs.inv"
        ),
    )
    parser.addoption("--nonloc", action="store_true", help="Include nonlocal tests")
    parser.addoption(
        "--flake8_ext", action="store_true", help="Include flake8 extensions test"
    )


@pytest.fixture(scope="session")
def res_path():
    """Provide Path object to the test resource directory."""
    return Path("tests", "resource")


@pytest.fixture(scope="session")
def res_cmp(res_path, misc_info):
    """Provide Path object to the compressed attrs inventory in resource."""
    return res_path / (misc_info.FNames.RES.value + misc_info.Extensions.CMP.value)


@pytest.fixture(scope="session")
def res_dec(res_path, misc_info):
    """Provide Path object to the decompressed attrs inventory in resource."""
    return res_path / (misc_info.FNames.RES.value + misc_info.Extensions.DEC.value)


@pytest.fixture(scope="session")
def misc_info(res_path):
    """Supply Info object with various test-relevant content."""

    class Info:
        """Monolithic test-information class."""

        class FNames(str, Enum):
            """Enum of test-relevant file names."""

            RES = "objects_attrs"
            INIT = "objects"
            MOD = "objects_mod"

        class Extensions(str, Enum):
            """Enum of test-relevant file extensions."""

            CMP = ".inv"
            DEC = ".txt"
            JSON = ".json"

        invalid_filename = "*?*?.txt" if sys.platform == "win32" else "/"

        IN_PYPY = "pypy" in sys.implementation.name

        # Sample object lines lines from an inventory, as bytes
        # False --> contracted abbreviations
        # True  --> expanded abbreviations
        byte_lines = {
            False: b"attr.Attribute py:class 1 api.html#$ -",
            True: b"attr.Attribute py:class 1 api.html#attr.Attribute attr.Attribute",
        }

        # For the URL mode of Inventory instantiation
        remote_url = (
            "https://github.com/bskinn/sphobjinv/raw/master/"
            "tests/resource/objects_{0}.inv"
        )

        # Regex pattern for objects_xyz.inv files
        p_inv = re.compile(r"objects_([^.]+)\.inv", re.I)

    # Standard location for the already-decompressed object in resource folder,
    # for comparison to a freshly generated decompressed file
    Info.res_decomp_path = res_path / (
        Info.FNames.RES.value + Info.Extensions.DEC.value
    )

    # String version of the sample object lines
    Info.str_lines = {_: Info.byte_lines[_].decode("utf-8") for _ in Info.byte_lines}

    return Info()


@pytest.fixture()
def scratch_path(tmp_path, res_path, misc_info):
    """Provision pre-populated scratch directory, returned as Path."""
    res_base = misc_info.FNames.RES.value
    scr_base = misc_info.FNames.INIT.value

    for ext in [_.value for _ in misc_info.Extensions]:
        # The str() calls here are for Python 3.5 compat
        shutil.copy(
            str(res_path / "{}{}".format(res_base, ext)),
            str(tmp_path / "{}{}".format(scr_base, ext)),
        )

    yield tmp_path


@pytest.fixture(scope="session")
def ensure_doc_scratch():
    """Ensure doc/scratch dir exists, for README shell examples."""
    Path("doc", "scratch").mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def bytes_txt(misc_info, res_path):
    """Load and return the contents of the example objects_attrs.txt as bytes."""
    return soi.fileops.readbytes(
        res_path / (misc_info.FNames.RES.value + misc_info.Extensions.DEC.value)
    )


@pytest.fixture(scope="session")
def sphinx_load_test():
    """Return function to perform 'live' Sphinx inventory load test."""
    from sphinx.util.inventory import InventoryFile as IFile

    def func(path):
        """Perform the 'live' inventory load test."""
        with path.open("rb") as f:
            try:
                IFile.load(f, "", osp.join)
            except Exception as e:  # noqa: PIE786
                # An exception here is a failing test, not a test error.
                pytest.fail(e)

    return func


@pytest.fixture()  # Must be function scope since uses monkeypatch
def run_cmdline_test(monkeypatch):
    """Return function to perform command line exit code test."""
    from sphobjinv.cli.core import main

    def func(arglist, *, expect=0):  # , suffix=None):
        """Perform the CLI exit-code test."""

        # Assemble execution arguments
        runargs = ["sphobjinv"]
        runargs.extend(str(a) for a in arglist)

        # Mock sys.argv, run main, and restore sys.argv
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", runargs)

            try:
                main()
            except SystemExit as e:
                retcode = e.args[0]
                ok = True
            else:
                ok = False

        # Do all pytesty stuff outside monkeypatch context
        assert ok, "SystemExit not raised on termination."

        # Test that execution completed w/indicated exit code
        assert retcode == expect, runargs

    return func


@pytest.fixture(scope="session")
def decomp_cmp_test(misc_info):
    """Return function to confirm a decompressed file is identical to resource."""

    def func(path):
        """Perform the round-trip compress/decompress comparison test."""
        # The str() calls here are for Python 3.5 compat
        assert cmp(str(misc_info.res_decomp_path), str(path), shallow=False)

    return func


@pytest.fixture(scope="session")
def attrs_inventory_test():
    """Provide function for high-level attrs Inventory consistency tests."""

    def func(inv, source_type):
        """Perform high-level attrs Inventory consistency test.

        `inv` is an Inventory instance.
        `source_type` is a member of the `soi.inventory.SourceTypes` enum.

        """
        assert inv.project == "attrs"
        assert inv.version == "17.2"
        assert inv.count == 56
        assert inv.source_type

    return func


testall_inv_paths = (
    p
    for p in (Path(__file__).parent / "tests" / "resource").iterdir()
    if p.name.startswith("objects_") and p.name.endswith(".inv")
)


@pytest.fixture(params=testall_inv_paths)
def testall_inv_path(request):
    """Provide parametrized --testall inventory paths."""
    return request.param


@pytest.fixture(scope="session")
def is_win():
    """Report boolean of whether the current system is Windows."""
    return platform.system().lower() == "windows"


@pytest.fixture(scope="session")
def unix2dos():
    """Provide function for converting POSIX to Windows EOLs."""
    return partial(re.sub, rb"(?<!\r)\n", b"\r\n")


@pytest.fixture(scope="session")
def jsonschema_validator():
    """Provide the standard JSON schema validator."""
    return jsonschema.Draft4Validator
