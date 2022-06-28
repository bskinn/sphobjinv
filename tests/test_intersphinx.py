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
    ("web_url", "inv_url", "project", "mapping"),
    [
        (
            "https://flask.palletsprojects.com/en/1.1.x/api/#flask.Config",
            "https://flask.palletsprojects.com/en/1.1.x/objects.inv",
            "flask",
            ("https://flask.palletsprojects.com/en/1.1.x/", None),
        ),
        (
            "https://docs.djangoproject.com/en/4.0/topics/cache/#memcached",
            "https://docs.djangoproject.com/en/4.0/_objects/",
            "django",
            (
                "https://docs.djangoproject.com/en/4.0/",
                "https://docs.djangoproject.com/en/4.0/_objects/",
            ),
        ),
        (
            (
                "https://docs.scipy.org/doc/numpy-1.13.0/reference/"
                "arrays.interface.html#python-side"
            ),
            "https://docs.scipy.org/doc/numpy-1.13.0/objects.inv",
            "numpy",
            ("https://docs.scipy.org/doc/numpy-1.13.0/", None),
        ),
    ],
    ids=(lambda arg: arg if (isinstance(arg, str) and "/" not in arg) else ""),
)
def test_infer_mapping(web_url, inv_url, project, mapping, res_path):
    """Confirm intersphinx mapping inference works for select test cases.

    These test(s) should continue to pass even if the various documentation sets
    on the web are taken down. ``web_url`` and ``inv_url`` are chosen to be
    valid and consistent with the versions of the |objects.inv| files stored
    in the tests resource path `res_path`.

    """
    inv_path = res_path / f"objects_{project}.inv"
    assert mapping == soi_isphx.infer_mapping(web_url, inv_url, soi.Inventory(inv_path))
