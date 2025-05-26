r"""*Direct, NONLOCAL expect-good API tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    21 Mar 2019

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

import sphobjinv as soi


pytestmark = [
    pytest.mark.api,
    pytest.mark.nonloc,
    pytest.mark.flaky(retries=2, delay=5),
]


@pytest.fixture(scope="module", autouse=True)
def skip_if_no_nonloc(pytestconfig):
    """Skip test if --nonloc not provided.

    Auto-applied to all functions in module, since module is nonlocal.

    """
    if not pytestconfig.getoption("--nonloc"):
        pytest.skip("'--nonloc' not specified")  # pragma: no cover


@pytest.mark.parametrize(
    ["name", "url"],
    [
        ("flask", "http://flask.palletsprojects.com/en/1.1.x/objects.inv"),
        ("h5py", "https://docs.h5py.org/en/stable/objects.inv"),
    ],
    ids=(lambda x: "" if "://" in x else x),
)
@pytest.mark.timeout(30)
def test_api_inventory_known_header_required(name, url):
    """Confirm URL load works on docs pages requiring HTTP header config."""
    inv = soi.Inventory(url=url)
    assert inv.count > 0


@pytest.mark.testall
@pytest.mark.timeout(30)
def test_api_inventory_many_url_imports(
    testall_inv_path,
    res_path,
    scratch_path,
    misc_info,
    sphinx_load_test,
    pytestconfig,
):
    """Confirm a plethora of .inv files downloads properly via url arg.

    This test is SLOW, and so does not run by default.  Invoke with `--nonloc`
    to run it; invoke with `--testall` to test over all .inv files in
    tests/resource.

    """
    fname = testall_inv_path.name
    scr_fpath = scratch_path / fname

    # Drop most unless testall
    if not pytestconfig.getoption("--testall") and fname != "objects_attrs.inv":
        pytest.skip("'--testall' not specified")

    # Construct inventories for comparison
    mch = misc_info.p_inv.match(fname)
    proj_name = mch.group(1)
    inv1 = soi.Inventory(str(res_path / fname))
    inv2 = soi.Inventory(url=misc_info.remote_url.format(proj_name))

    # Test the things
    assert inv1 == inv2

    # Ensure sphinx likes the regenerated inventory
    data = inv2.data_file()
    cmp_data = soi.compress(data)
    soi.writebytes(scr_fpath, cmp_data)
    sphinx_load_test(scr_fpath)
