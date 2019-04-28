r"""*Test(s) to ensure full loading of flake8 extensions*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    27 Apr 2019

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

import re
import subprocess as sp
import urllib.request as urlrq

import certifi
import pytest


@pytest.fixture(scope="module", autouse=True)
def skip_if_no_nonloc(pytestconfig):
    """Skip test if --nonloc not provided.

    Auto-applied to all functions in module, since module is nonlocal.

    """
    if not pytestconfig.getoption("--nonloc"):
        pytest.skip("'--nonloc' not specified")


@pytest.fixture()
def testmodule(tmp_path):
    """Retrieve the flake8 extension test module as a BytesIO."""
    main_page = urlrq.urlopen(
        "https://gist.github.com/bskinn/ab328d0d9233586641455ac73056f946",
        cafile=certifi.where(),
    ).read()
    raw_url_tail = re.search(rb'"([^"]+/raw/[^"]+)"', main_page, re.I).group(1)
    module_contents = urlrq.urlopen(
        "https://gist.github.com" + raw_url_tail.decode(), cafile=certifi.where()
    ).read()
    testmod_path = tmp_path / "flake8_ext_test.py"

    with testmod_path.open("wb") as f:
        f.write(module_contents)

    # ~ with testmod_path.open() as f:
    # ~ yield f
    yield testmod_path


@pytest.mark.nonloc
@pytest.mark.timeout(10)
def test_flake8_extensions(testmodule, subtests, tmp_path):
    """Check the flake8 extension tester module and confirm all expected reports.

    This test is set up to retrieve the file from gist because it would be
    annoying to keep it in-repo: the flake8 config would take all sorts of rejiggering.

    """
    expected_errors = """

    (core flake8)
    flake8/pyflakes         F401, W293
    pycodestyle             E501
    mccabe                  C901

    (extensions)
    flake8-bandit           S110
    flake8-black            BLK100
    flake8-bugbear          B006
    flake8-builtins         A002
    flake8-comprehensions   C400
    flake8-docstrings       D103
    flake8-eradicate        E800
    flake8-import-order     I100
    flake8-pie              PIE781
    flake8-rst-docstrings   RST212
    pep8-naming             N802

    """
    try:
        sp.check_output(
            ["flake8 --max-complexity 1 {}".format(str(testmodule.resolve()))],
            shell=True,
        )
    except sp.CalledProcessError as e:
        retcode = e.returncode
        output = e.output.decode()
    else:
        pytest.fail("Test file unexpectedly passed flake8 check.")

    assert 1 == retcode

    for code in (
        _.group(0) for _ in re.finditer(r"[A-Z]{1,3}[0-9]{1,3}", expected_errors)
    ):
        with subtests.test(id=code):
            assert code in output
