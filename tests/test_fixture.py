r"""*Trivial fixture tests for* ``sphobjinv``.

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

import pytest

pytestmark = pytest.mark.fixture


def test_info_fixture(misc_info):
    """Confirm arbitrary member of misc_info fixture."""
    assert True in misc_info.byte_lines


def test_populate_scratch(misc_info, scratch_path, check):
    """Ensure the scratch_path fixture populates the scratch dir correctly."""
    scr_base = misc_info.FNames.INIT.value

    for ext in [_.value for _ in misc_info.Extensions]:
        with check(msg=ext):
            assert (scratch_path / f"{scr_base}{ext}").is_file(), ext


def test_sphinx_load(res_path, sphinx_load_test):
    """Confirm sphinx_load_test fixture works on known-good inventory."""
    sphinx_load_test(res_path / "objects_attrs.inv")


def test_cli_invoke(run_cmdline_test):
    """Confirm CLI test with no args exits ok.

    Should just print help and exit.

    """
    run_cmdline_test([])


def test_decomp_comp_fixture(misc_info, decomp_cmp_test, scratch_path):
    """Test decomp_cmp_test works in 'identity' case.

    Basically is telling filecmp.cmp to compare a reference inventory file
    with itself.

    """
    decomp_cmp_test(
        scratch_path / f"{misc_info.FNames.INIT.value}{misc_info.Extensions.DEC.value}"
    )
