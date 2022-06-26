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


pytestmark = [pytest.mark.intersphinx, pytest.mark.local]


@pytest.mark.parametrize(
    ("uri", "trimmed"),
    [("cli/implementation/parser.html#$", "cli/implementation/parser.html")],
)
def test_object_uri_trim(uri, trimmed):
    """Confirm that object URI trimming is working."""
    assert trimmed == soi_isphx._strip_url_to_netloc_path(uri)


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
    assert trimmed == soi_isphx._extract_objectsinv_url_base(url)


@pytest.mark.parametrize(
    ("web_url", "inv_url", "result", "project"),
    [
        (
            "https://www.attrs.org/en/17.2.0/api.html#attr.s",
            "https://www.attrs.org/en/17.2.0/objects.inv",
            True,
            "attrs",
        )
    ],
)
def test_url_matchup_local(web_url, inv_url, result, project, res_path):
    """Confirm that URL matching works for selected test/resource inventories.

    These test(s) should continue to pass even if the various documentation sets
    on the web are taken down. ``web_url`` and ``inv_url`` are chosen to be
    valid and consistent with the versions of the |objects.inv| files stored
    in ``tests/resource/``.

    """
    inv_path = res_path / f"objects_{project}.inv"
    assert result == soi_isphx._url_matchup(web_url, inv_url, soi.Inventory(inv_path))
