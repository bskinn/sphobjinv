r"""*Hypothesis tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    9 Feb 2021

**Copyright**
    \(c) Brian Skinn 2016-2021

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import os.path as osp
from io import BytesIO

import pytest
from hypothesis import given, settings, strategies as st
from sphinx.util.inventory import InventoryFile as IFile

import sphobjinv as soi

# Unicode categories at: http://www.unicode.org/reports/tr44/#GC_Values_Table
@given(
    st.text(min_size=1, alphabet=st.characters(blacklist_categories=("C", "Zl", "Zp"))),
    st.text(min_size=1, alphabet=st.characters(whitelist_categories=("L", "N"))),
    st.text(min_size=1, alphabet=st.characters(whitelist_categories=("L", "N"))),
    st.integers(),
    st.text(),
    st.text(min_size=1, alphabet=st.characters(blacklist_categories=("C", "Zl", "Zp"))),
)
@settings(max_examples=400)
def test_hypothesis_dataobjstr_instantiate(
    misc_info, sphinx_ifile_data_count, name, domain, role, priority, uri, dispname
):
    """Run hypothesis tests over simple DataObjStr instantiation."""
    dos = soi.DataObjStr(
        name=name,
        domain=domain,
        role=role,
        priority=str(priority),
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
