r"""*Valid/invalid object data tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    13 Feb 2021

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
import zlib
from io import BytesIO

import pytest
import sphinx
from sphinx.util.inventory import InventoryFile as IFile

import sphobjinv as soi


@pytest.fixture(autouse=True)
def skip_on_sphinx_version(sphinx_version):
    """Trigger test skip if Sphinx version is too low.

    Changes to the Sphinx InventoryFile regex &c. cause older
    versions of Sphinx to have different behavior.

    This skip *should* only trigger during the tox matrix of
    environments with various old dependency versions.

    """
    if sphinx_version < (3, 3, 0):  # pragma: no cover
        pytest.skip("Sphinx version too low")


# Once DataObjStr instance validation is in place, this will probably
# be a good place to use hypothesis
@pytest.mark.parametrize(
    ("name", "domain", "role", "prio", "uri", "dispname"),
    [
        ("foo", "py", "data", 1, "quux.html#$", "-"),  # Priorities
        ("foo", "py", "data", 0, "quux.html#$", "-"),
        ("foo", "py", "data", -1, "quux.html#$", "-"),
        ("foo", "py", "data", -1235778, "quux.html#$", "-"),
        ("foo", "py", "data", 2214888, "quux.html#$", "-"),
        ("foo bar", "std", "term", 1, "quux.html#$", "-"),  # Space in name
        ("foo\tbar", "std", "term", 1, "quux.html#$", "-"),  # Valid but discouraged
        ("Index Page", "std", "doc", 1, "index.html", "-"),
        ("Index Page", "std", "doc", 1, "index.html", "Index Page Thing"),
        ("Index Page", "std", "doc", 1, "index.html", "Index\tPage\tThing"),
        ("Index Page", "std", "doc", 1, "", "-"),  # Zero-length uri
        ("Index # Page", "std", "doc", 1, "index.html", "-"),  # Symbol in name
        ("Thing \u33a4", "std", "ref", 1, "index.html#$", "-"),  # Unicode in name
        ("Thing One", "std", "ref", 1, "index.html#$", "\u33a4"),  # Unicode in dispname
        ("foo", "py", "da:ta", 1, "data.html#$", "-"),  # Colon in role (used in Sphinx)
        ("foo", "py$", "data", 1, "data.html#$", "-"),  # Valid but discouraged
        ("foo", "py\u33a4", "data", 1, "data.html#$", "-"),  # Valid but discouraged
        ("foo", "py", "data$", 1, "data.html#$", "-"),  # Valid but discouraged
        ("foo", "py", "data\u33a4", 1, "data.html#$", "-"),  # Valid but discouraged
        ("foo", "py", "data", 1, "data/\u33a4.html#$", "-"),  # Valid but discouraged
        ("  foo", "py", "data", 1, "data.html#$", "-"),  # Valid but discouraged
        # Colon in domain (invalid but undetectable)
        ("foo", "p:y", "data", 1, "data.html#$", "-"),
    ],
)
def test_dataobjstr_valid_objects(
    misc_info, sphinx_ifile_data_count, name, domain, role, prio, uri, dispname
):
    """Run sphobjinv/sphinx comparison on specific object data lines."""
    dos = soi.DataObjStr(
        name=name,
        domain=domain,
        role=role,
        priority=str(prio),
        uri=uri,
        dispname=dispname,
    )

    assert dos

    inv = soi.Inventory()
    inv.project = "Foo"
    inv.version = "1.0"
    inv.objects.append(
        soi.DataObjStr(
            name="bar", domain="py", role="data", priority="1", uri="$", dispname="-"
        )
    )
    inv.objects.append(dos)

    df = inv.data_file(contract=True)

    ifile_data = IFile.load(BytesIO(soi.compress(df)), "", osp.join)

    ifile_count = sphinx_ifile_data_count(ifile_data)

    assert inv.count == ifile_count

    domrole = "{dos.domain}:{dos.role}".format(dos=dos)

    assert domrole in ifile_data
    assert dos.name in ifile_data[domrole]


@pytest.mark.parametrize(
    ("name", "domain", "role", "prio", "uri", "dispname"),
    [
        ("", "std", "doc", 1, "index.html", "-"),  # Missing name
        ("foo  ", "py", "data", 1, "data.html#$", "-"),  # Name w/trailing space
        ("# Index Page", "std", "doc", 1, "index.html", "-"),  # '#' @ name start
        ("X Y Z 0 foo", "std", "doc", 1, "index.html", "-"),  # Int in name
        ("foo", "py thon", "data", 1, "data.html#$", "-"),  # Space in domain
        ("foo", "", "data", 1, "data.html#$", "-"),  # Missing domain
        ("foo", "py", "da ta", 1, "data.html#$", "-"),  # Space in role
        ("foo", "py", "", 1, "data.html#$", "-"),  # Missing role
        ("foo", "py", "data", 0.5, "data.html#$", "-"),  # Non-integer prio
        ("foo", "py", "data", "", "data.html#$", "-"),  # Missing prio
        ("foo", "py", "data", "quux", "data.html#$", "-"),  # Non-numeric prio
        ("Index Page", "std", "doc", 1, "index.html", ""),  # Missing dispname
        ("Index Page", "std", "doc", 1, "", ""),  # Missing uri & dispname
    ],
)
def test_dataobjstr_invalid_objects(
    misc_info, sphinx_ifile_data_count, name, domain, role, prio, uri, dispname
):
    """Run sphobjinv/sphinx comparison on specific invalid data lines."""
    with pytest.raises((AssertionError, zlib.error)):
        test_dataobjstr_valid_objects(
            misc_info, sphinx_ifile_data_count, name, domain, role, prio, uri, dispname
        )


def int_to_latin_1(val):
    """Provide the latin-1 string equivalent of an 8-bit int."""
    return bytes((val,)).decode("latin-1")


def latin_1_id(val):
    """Provide the value-and-character string for a latin-1 int value."""
    return str(val) + "_" + int_to_latin_1(val)


@pytest.mark.parametrize("leadint", range(255), ids=latin_1_id)
def test_name_lead_chars(misc_info, sphinx_ifile_data_count, leadint):
    """Screen for valid/invalid first characters."""
    name = int_to_latin_1(leadint) + " foo"

    # For Sphinx < 8.2 expect only two fail cases, newline and '#'
    if leadint in (10, 35):
        pytest.xfail("Known invalid name lead char")

    # Sphinx >= 8.2 uses splitlines(), which strips more line boundary characters.
    # See https://github.com/bskinn/sphobjinv/issues/314
    if sphinx.version_info >= (8, 2) and leadint in (11, 12, 13, 28, 29, 30, 133):
        pytest.xfail(
            "Known invalid name lead char for Sphinx >= 8.2"
        )  # pragma: no cover

    test_dataobjstr_valid_objects(
        misc_info,
        sphinx_ifile_data_count,
        name=name,
        domain="py",
        role="data",
        prio=1,
        uri="data.html#$",
        dispname="-",
    )
