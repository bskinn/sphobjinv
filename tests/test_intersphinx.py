r"""*Tests for intersphinx-related functionality for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    21 Jun 2022

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

import pytest

import sphobjinv.cli.suggest as soi_cli_suggest


pytestmark = [pytest.mark.intersphinx, pytest.mark.local]


@pytest.mark.parametrize(
    ("uri", "trimmed", "with_scheme"),
    [
        ("cli/implementation/parser.html#$", "cli/implementation/parser.html", False),
        (
            (
                "https://sphobjinv.readthedocs.io/en/stable/api/"
                "enum.html#sphobjinv.enum.HeaderFields"
            ),
            "//sphobjinv.readthedocs.io/en/stable/api/enum.html",
            False,
        ),
        (
            (
                "https://sphobjinv.readthedocs.io/en/stable/api/"
                "enum.html#sphobjinv.enum.HeaderFields"
            ),
            "https://sphobjinv.readthedocs.io/en/stable/api/enum.html",
            True,
        ),
    ],
)
def test_strip_netloc_path(uri, trimmed, with_scheme):
    """Confirm that object URI trimming is working."""
    assert trimmed == soi_cli_suggest._strip_url_to_netloc_path(
        uri, with_scheme=with_scheme
    )


@pytest.mark.parametrize(
    ("url", "trimmed"),
    [
        (
            "https://sphobjinv.readthedocs.io/en/latest/objects.inv",
            "https://sphobjinv.readthedocs.io/en/latest/",
        )
    ],
)
def test_extract_objinv_url_base(url, trimmed):
    """Confirm that inventory URL trimming is working."""
    assert trimmed == soi_cli_suggest.extract_objectsinv_url_base(url)
