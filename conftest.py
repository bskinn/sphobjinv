r"""*Root conftest for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    20 Mar 2019

**Copyright**
    \(c) Brian Skinn 2016-2019

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from enum import Enum
import sys

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--testall",
        action="store_true",
        help="Test *all* inventories stored in testing resource folder",
    )


@pytest.fixture()
def scratch_dir(tmp_path):
    pass


@pytest.fixture(scope="session")
def fnames():
    class FNames(Enum):
        RES_FNAME_BASE = "objects_attrs"
        INIT_FNAME_BASE = "objects"
        MOD_FNAME_BASE = "objects_mod"

    return FNames


@pytest.fixture(scope="session")
def exts():
    class Extensions(Enum):
        CMP_EXT = ".inv"
        DEC_EXT = ".txt"
        JSON_EXT = ".json"

    return Extensions


@pytest.fixture(scope="session")
def invalid_fname():
    "*?*?.txt" if sys.platform == "win32" else "/"


@pytest.fixture(scope="session")
def byte_lines():
    """True gives expanded bytes object info line; False gives contracted."""
    return {
        False: b"attr.Attribute py:class 1 api.html#$ -",
        True: b"attr.Attribute py:class 1 api.html#attr.Attribute "
        b"attr.Attribute",
    }


@pytest.fixture(scope="session")
def str_lines(byte_lines):
    """True gives expanded str object info line; False gives contracted."""
    return {_: byte_lines[_].decode("utf-8") for _ in byte_lines}


# RESUME AT REMOTE_URL
