r"""*README shell command doctests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    6 Aug 2018

**Copyright**
    \(c) Brian Skinn 2016-2020

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
import subprocess as sp  # noqa: S404
from pathlib import Path


import pytest
from sphinx import __version__ as sphinx_ver


reqs = Path("requirements-dev.txt").read_text()

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


@pytest.mark.skipif(
    sphinx_ver != sphinx_req,
    reason="Skip if Sphinx version mismatches current dev version.",
)
def test_readme_shell_cmds(ensure_doc_scratch, subtests):
    """Perform testing on README shell command examples."""
    with open("README.rst") as f:
        text = f.read()

    chk = dt.OutputChecker()

    dt_flags = dt.ELLIPSIS | dt.NORMALIZE_WHITESPACE

    for i, mch in enumerate(p_shell.finditer(text)):
        cmd = mch.group("cmd")
        out = mch.group("out")

        proc = sp.run(  # noqa: S603
            shlex.split(cmd), stdout=sp.PIPE, stderr=sp.STDOUT, timeout=30
        )

        result = proc.stdout.decode("utf-8")

        msg = "\n\nExpected:\n" + out + "\n\nGot:\n" + result

        with subtests.test(i=i):
            assert chk.check_output(out, result, dt_flags), msg
