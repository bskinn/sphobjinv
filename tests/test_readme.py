r"""*README shell command doctests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    6 Aug 2018

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

import doctest as dt
import re
import shlex
import subprocess as sp
import sys
from textwrap import dedent


import pytest
from sphinx import __version__ as sphinx_ver

with open("requirements-dev.txt", "r") as f:
    reqs = f.read()

m_sphinx_req = re.search("^sphinx==(.+)$", reqs, re.I | re.M)
sphinx_req = m_sphinx_req.group(1)


p_shell = re.compile(
    r"""
    \n\s+[$](?P<cmd>.*)        # Entered command
    (?P<out>(\n.*)+?)          # Line(s) of output
    (?=\n\.\.)                 # Lookahead for explicit shell block endpoint
    """,
    re.X,
)


py_ver = sys.version_info


@pytest.mark.skipif(
    py_ver[0] < 3
    or (py_ver[0] == 3 and py_ver[1] < 5)
    or sphinx_ver != sphinx_req,
    reason="Skip on Python 3.4 and below due to variant subprocess behavior, "
    "and skip if Sphinx version mismatches current dev version.",
)
def test_readme_shell_cmds(ensure_doc_scratch):
    """Perform testing on README shell command examples."""
    with open("README.rst") as f:
        text = f.read()

    chk = dt.OutputChecker()

    dt_flags = dt.ELLIPSIS | dt.NORMALIZE_WHITESPACE

    for mch in p_shell.finditer(text):
        cmd = mch.group("cmd")
        out = mch.group("out")

        proc = sp.run(
            shlex.split(cmd), stdout=sp.PIPE, stderr=sp.STDOUT, timeout=30
        )

        result = proc.stdout.decode("utf-8")

        msg = "\n\nExpected:\n" + out + "\n\nGot:\n" + result

        assert chk.check_output(out, result, dt_flags), msg


if __name__ == "__main__":
    print("Module not executable.")
