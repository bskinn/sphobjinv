r"""*Root conftest for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    20 Mar 2019

**Copyright**
    \(c) Brian Skinn 2016-2025

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

**Members**

"""

import os.path as osp
import platform
import re
import shutil
import sys
from enum import Enum
from functools import partial
from io import BytesIO
from pathlib import Path

import jsonschema
import pytest
from sphinx import __version__ as sphinx_version_str
from sphinx.util.inventory import InventoryFile as IFile

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
            "https://github.com/bskinn/sphobjinv/raw/main/"
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
def scratch_path(tmp_path, res_path, misc_info, is_win, unix2dos):
    """Provision pre-populated scratch directory, returned as Path."""
    res_base = misc_info.FNames.RES.value
    scr_base = misc_info.FNames.INIT.value

    for ext in [_.value for _ in misc_info.Extensions]:
        # The str() calls here are for Python 3.5 compat
        shutil.copy(
            str(res_path / f"{res_base}{ext}"),
            str(tmp_path / f"{scr_base}{ext}"),
        )

    # With the conversion of resources/objects_attrs.txt to Unix EOLs in order to
    # provide for a Unix-testable sdist, on Windows systems this resource needs
    # to be converted to DOS EOLs for consistency.
    if is_win:
        win_path = tmp_path / f"{scr_base}{misc_info.Extensions.DEC.value}"
        win_path.write_bytes(unix2dos(win_path.read_bytes()))

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


def sphinx_ifile_load(path):
    """Carry out inventory load via Sphinx InventoryFile.

    Defined as a standalone function to allow importing
    during debugging.

    """
    return IFile.load(BytesIO(path.read_bytes()), "", osp.join)


@pytest.fixture(scope="session", name="sphinx_ifile_load")
def fixture_sphinx_ifile_load():
    """Return helper function to load inventory via Sphinx InventoryFile."""
    return sphinx_ifile_load


def sphinx_ifile_data_count(ifile_data):
    """Report the total number of items in the InventoryFile data.

    Defined standalone to allow import during debugging.

    """
    return sum(len(ifile_data[k]) for k in ifile_data)


@pytest.fixture(scope="session", name="sphinx_ifile_data_count")
def fixture_sphinx_ifile_data_count():
    """Return helper function to report total number of objects."""
    return sphinx_ifile_data_count


@pytest.fixture(scope="session")
def sphinx_load_test(sphinx_ifile_load):
    """Return function to perform 'live' Sphinx inventory load test."""

    def func(path):
        """Perform the 'live' inventory load test."""
        try:
            sphinx_ifile_load(path)
        except Exception as e:  # noqa: PIE786
            # An exception here is a failing test, not a test error.
            pytest.fail(e)

    return func


@pytest.fixture(scope="session")
def sphinx_version():
    """Provide the installed Sphinx version as a tuple.

    Returns (major, minor, patch).

    """
    p_version = re.compile(r"(\d+)[.]?(\d+)?[.]?(\d+)?")
    mch = p_version.match(sphinx_version_str)
    return tuple(int(x) if x else 0 for x in mch.groups())


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
def decomp_cmp_test(misc_info, is_win, unix2dos):
    """Return function to confirm a decompressed file is identical to resource."""

    def func(path):
        """Perform the round-trip compress/decompress comparison test."""
        # The str() calls here are for Python 3.5 compat
        res_bytes = Path(misc_info.res_decomp_path).read_bytes()
        tgt_bytes = Path(path).read_bytes()  # .replace(b"\r\n", b"\n")

        if is_win:
            # Have to explicitly convert these newlines, now that the
            # tests/resource/objects_attrs.txt file is marked 'binary' in
            # .gitattributes
            res_bytes = unix2dos(res_bytes)

        assert res_bytes == tgt_bytes

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
        assert inv.version == "22.1"
        assert inv.count == 129
        assert inv.source_type

    return func


testall_inv_paths = [
    p
    for p in (Path(__file__).parent / "tests" / "resource").iterdir()
    if p.name.startswith("objects_") and p.name.endswith(".inv")
]
testall_inv_ids = [p.name[8:-4] for p in testall_inv_paths]


@pytest.fixture(params=testall_inv_paths, ids=testall_inv_ids)
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
