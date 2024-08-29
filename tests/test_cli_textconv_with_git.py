r"""*CLI tests for* ``sphobjinv-textconv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

``sphobjinv-textconv`` is a strictly limited subset of
``sphobjinv`` expects an INFILE inventory, converts it, then writes to
stdout. Intended for use with git diff. git, detect changes, by first
converting an (partially binary) inventory to plain text.

**Author**
    Dave Faulkmore (msftcangoblowme@protonmail.com)

**File Created**
    23 Aug 2024

**Copyright**
    \(c) Brian Skinn 2016-2024

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

.. code-block:: shell

   pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
   --cov-config=pyproject.toml --nonloc tests

**Members**

"""
import logging
import re
import shutil

import pytest

from .wd_wrapper import (  # noqa: ABS101
    run,
    WorkDir,
)

logger = logging.getLogger(__name__)


@pytest.fixture()
def caplog_configure(caplog):
    """Config logging and caplog fixture."""
    caplog.set_level(logging.INFO)


class TestTextconvIntegration:
    """Prove git diff an compare |objects.inv| files."""

    def test_textconv_git_diff(
        self,
        caplog,
        caplog_configure,
        misc_info,
        scratch_path,
        res_cmp_plus_one_line,
        gitconfig,
        gitattributes,
        is_win,
        is_linux,
    ):
        """Demonstrate git diff on a zlib inventory.

        .. code-block:: shell

           pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
           -vv --cov-config=pyproject.toml -k test_textconv_git_diff tests

        """
        # word placeholder --> \w+
        # Escape $ --> \$
        # Escape + --> \+
        expected_diff = (
            r"^diff --git a/objects\.inv b/objects\.inv\r?\n"
            r"index \w+\.\.\w+ \w+\r?\n"
            r"\-\-\- a/objects\.inv\r?\n"
            r"\+\+\+ b/objects\.inv\r?\n"
            r"@@ \-131,4 \+131,5 @@ types std:doc \-1 types\.html Type Annotations\r?\n"
            r" validators std:label \-1 init\.html\#\$ Validators\r?\n"
            r" version-info std:label \-1 api\.html\#\$ \-\r?\n"
            r" why std:doc \-1 why\.html Why not…\r?\n"
            r"\+attrs\.validators\.set_cheat_mode py:function 1 api\.html\#\$ \-\r?\n"
            r" \r?\n$"
        )

        # prepare
        #    project folder
        path_cwd = scratch_path
        wd = WorkDir(path_cwd)
        if is_win or is_linux:
            msg_info = f"cwd {wd.cwd!s}"
            logger.info(msg_info)

        #    On Windows, unresolved executables paths
        soi_textconv_path = "sphobjinv-textconv"

        #    On Windows, resolved executables paths
        resolved_soi_textconv_path = shutil.which(soi_textconv_path)
        if resolved_soi_textconv_path is None:
            resolved_soi_textconv_path = soi_textconv_path

        #    git init
        wd("git init")
        wd("git config user.email test@example.com")
        wd('git config user.name "a test"')

        #    .git/config
        #    defines the diff textconv "inv"
        path_git_config = gitconfig(wd.cwd)
        git_config_contents = path_git_config.read_text()
        assert """[diff "inv"]""" in git_config_contents

        #    .gitattributes
        #    Informs git: .inv are binary files uses textconv "inv" from .git/config
        path_ga = gitattributes(wd.cwd)
        git_attributes_contents = path_ga.read_text()
        assert "*.inv binary diff=inv" in git_attributes_contents

        #     scratch_path from objects_attrs.{inv|txt|json}
        #     creates: objects.inv, objects.txt, and objects.json
        path_fname_src = misc_info.FNames.INIT + misc_info.Extensions.CMP
        path_cmp_dst = wd.cwd / path_fname_src

        objects_inv_size_before = path_cmp_dst.stat().st_size

        #    commit (1st)
        wd.add_command = "git add ."
        wd.commit_command = "git commit --no-verify --no-gpg-sign -m test-{reason}"
        wd.add_and_commit(reason="sphobjinv-textconv", signed=False)

        # overwrite objects.inv (aka path_cmp_dst)
        res_cmp_plus_one_line(wd.cwd)

        objects_inv_size_after = path_cmp_dst.stat().st_size
        reason = f"objects.inv supposed to have been overwritten {path_cmp_dst}"
        assert objects_inv_size_before != objects_inv_size_after, reason

        #    Compare last commit .inv with updated .inv
        #    If virtual environment not activated, .git/config texconv
        #    executable relative path will not work e.g. sphobjinv-textconv
        #
        #    error: cannot run sphobjinv-textconv: No such file or directory
        #    fatal: unable to read files to diff
        #    exit code 128
        cmd = f"git diff HEAD {path_cmp_dst.name}"
        sp_out = run(cmd, cwd=wd.cwd)
        retcode = sp_out.returncode
        out = sp_out.stdout

        #    Diagnostics before assertions
        #    On error, not showing locals, so print source file and diff
        if is_win or is_linux:
            msg_info = f"cmd: {cmd}"
            logger.info(msg_info)
            msg_info = f"diff: {out}"
            logger.info(msg_info)
            msg_info = f"regex: {expected_diff}"
            logger.info(msg_info)
            msg_info = f"out: {out}"
            logger.info(msg_info)
            logging_records = caplog.records  # noqa: F841

        assert retcode == 0
        assert len(out) != 0

        # Had trouble finding executable's path. On Windows, regex should be OK
        pattern = re.compile(expected_diff)
        lst_matches = pattern.findall(out)
        assert lst_matches is not None
        assert isinstance(lst_matches, list)
        assert len(lst_matches) == 1