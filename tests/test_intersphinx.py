r"""*Tests for intersphinx-related functionality for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    21 Jun 2022

**Copyright**
    \(c) Brian Skinn 2016-2022

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import pytest

import sphobjinv as soi
import sphobjinv.intersphinx as soi_isphx


pytestmark = [pytest.mark.intersphinx]


@pytest.mark.local
@pytest.mark.parametrize(
    ("uri", "trimmed"),
    [("cli/implementation/parser.html#$", "cli/implementation/parser.html")],
)
def test_object_uri_trim(uri, trimmed):
    """Confirm that object URI trimming is working."""
    assert trimmed == soi_isphx._trim_object_uri(uri)


@pytest.mark.local
@pytest.mark.parametrize(
    ("url", "trimmed"),
    [
        (
            "https://sphobjinv.readthedocs.io/en/latest/objects.inv",
            "https://sphobjinv.readthedocs.io/en/latest/",
        )
    ],
)
def test_inventory_url_trim(url, trimmed):
    """Confirm that inventory URL trimming is working."""
    assert trimmed == soi_isphx._inventory_url_base(url)


@pytest.mark.nonloc
@pytest.mark.parametrize(
    ("web_url", "inv_url", "result"),
    [
        (
            (
                "https://sphobjinv.readthedocs.io/en/stable/api/"
                "error.html#sphobjinv.error.VersionError"
            ),
            "https://sphobjinv.readthedocs.io/en/stable/objects.inv",
            True,
        )
    ],
)
def test_url_matchup(web_url, inv_url, result, pytestconfig):
    """Confirm that URL matching works for known-good case."""
    if not pytestconfig.getoption("--nonloc"):
        pytest.skip("'--nonloc' not specified")  # pragma: no cover

    assert soi_isphx._url_matchup(web_url, inv_url, soi.Inventory(url=inv_url))
