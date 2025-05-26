r"""*Test(s) to ensure full loading of flake8 extensions*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    27 Apr 2019

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

import re
import subprocess as sp  # noqa: S404
import sys
from pathlib import Path

import pytest

pytestmark = [pytest.mark.flake8_ext]


@pytest.fixture(scope="module", autouse=True)
def skip_if_no_flake8_ext(pytestconfig):
    """Skip test if --flake8_ext not provided.

    Auto-applied to all functions in module.

    """
    if not pytestconfig.getoption("--flake8_ext"):
        pytest.skip("'--flake8_ext' not specified")  # pragma: no cover


@pytest.mark.skipif(
    sys.version_info < (3, 6),
    reason="Some flake8 extensions require Python 3.6 or later",
)
def test_flake8_version_output(check):
    """Confirm that all desired plugins actually report as loaded."""
    p_pkgname = re.compile("^[0-9a-z_-]+", re.I)
    plugins = Path("requirements-flake8.txt").read_text().splitlines()[1:]
    plugins = [p_pkgname.search(p).group(0) for p in plugins]

    # This is fragile if anything ends up not having a prefix that needs
    # stripping
    plugins = [p.partition("flake8-")[-1] for p in plugins]

    flake8_ver_output = sp.check_output(  # noqa: S607,S603
        ["flake8", "--version"], universal_newlines=True
    )  # noqa: S607,S603

    for p in plugins:
        with check(msg=p):
            assert p in flake8_ver_output.replace("_", "-").replace("\n", "")
