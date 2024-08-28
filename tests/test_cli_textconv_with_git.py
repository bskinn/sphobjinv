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
import os
import platform
import re
import shutil
import sys
from pathlib import Path

from sphobjinv import DataObjStr, Inventory
from sphobjinv.cli.load import import_infile
from sphobjinv.cli.write import write_plaintext

from .wd_wrapper import (  # noqa: ABS101
    run,
    WorkDir,
)


class TestTextconvIntegration:
    """Prove git diff an compare |objects.inv| files."""

    def test_textconv_git_diff(
        self,
        misc_info,
        scratch_path,
    ):
        """Demonstrate git diff on a zlib inventory.

        .. code-block:: shell

           pytest --showlocals --cov=sphobjinv --cov-report=term-missing \
           --cov-config=pyproject.toml -k test_textconv_git_diff tests

        """
        sep = os.linesep
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

        #    On Windows, unresolved executables paths
        soi_path = "sphobjinv"
        soi_textconv_path = "sphobjinv-textconv"

        #    On Windows, resolved executables paths
        resolved_soi_textconv_path = shutil.which(soi_textconv_path)
        if resolved_soi_textconv_path is None:
            resolved_soi_textconv_path = soi_textconv_path
        resolved_soi_path = shutil.which(soi_path)
        if resolved_soi_path is None:
            resolved_soi_path = soi_path

        #    git init
        wd("git init")
        wd("git config user.email test@example.com")
        wd('git config user.name "a test"')

        #    inventories: .txt and .inv
        # scratch_path copied:
        # objects_attrs.{.txt|.inv.json} --> objects.{.txt|.inv.json}
        path_cmp = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.CMP)
        dst_cmp_path = str(path_cmp)

        path_dec = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.DEC)
        dst_dec_path = str(path_dec)

        #    .git/config append
        path_git_config = path_cwd / ".git" / "config"
        str_git_config = path_git_config.read_text()

        #    On Windows, RESOLVED path necessary
        lines = [
            """[diff "inv"]""",
            f"""	textconv = {resolved_soi_textconv_path}""",
        ]

        gc_textconv = sep.join(lines)
        str_git_config = f"{str_git_config}{sep}{gc_textconv}{sep}"
        path_git_config.write_text(str_git_config)
        if platform.system() in ("Linux", "Windows"):
            print(f"executable path: {resolved_soi_textconv_path}", file=sys.stderr)
            print(f"""PATHEXT: {os.environ.get("PATHEXT", None)}""", file=sys.stderr)
            print(f".git/config {str_git_config}", file=sys.stderr)

        #    .gitattributes
        #    Informs git: .inv are binary files and which cmd converts .inv --> .txt
        path_ga = path_cwd / ".gitattributes"
        path_ga.touch()
        str_gitattributes = path_ga.read_text()
        ga_textconv = "*.inv binary diff=inv"
        str_gitattributes = f"{str_gitattributes}{sep}{ga_textconv}"
        wd.write(".gitattributes", str_gitattributes)

        #    commit (1st)
        wd.add_command = "git add ."
        wd.commit_command = "git commit --no-verify --no-gpg-sign -m test-{reason}"
        wd.add_and_commit(reason="sphobjinv-textconv", signed=False)

        # Act
        #    make change to .txt inventory (path_dst_dec)
        inv_0 = import_infile(dst_dec_path)
        obj_datum = DataObjStr(
            name="attrs.validators.set_cheat_mode",
            domain="py",
            role="function",
            priority="1",
            uri="api.html#$",
            dispname="-",
        )
        inv_0.objects.append(obj_datum)
        write_plaintext(inv_0, dst_dec_path)
        inv_0_count = len(inv_0.objects)
        inv_0_last_three = inv_0.objects[-3:]

        #    plain --> zlib
        if platform.system() in ("Linux", "Windows"):
            msg_info = f"objects dec before (count {inv_0_count}): {inv_0_last_three!r}"
            print(msg_info, file=sys.stderr)
            msg_info = f"size (dec): {path_dec.stat().st_size}"
            print(msg_info, file=sys.stderr)
            lng_cmd_size_before = path_cmp.stat().st_size
            msg_info = f"size (cmp): {lng_cmd_size_before}"
            print(msg_info, file=sys.stderr)

        # On Windows, UNRESOLVED path necessary
        cmd = f"{soi_path} convert -q zlib {dst_dec_path} {dst_cmp_path}"
        wd(cmd)

        inv_1 = Inventory(path_cmp)
        inv_1_count = len(inv_1.objects)
        inv_1_last_three = inv_1.objects[-3:]
        assert inv_0_count == inv_1_count
        assert inv_0_last_three == inv_1_last_three

        if platform.system() in ("Linux", "Windows"):
            msg_info = (
                f"objects after (count {inv_1_count}; delta"
                f"{inv_1_count - inv_0_count}): {inv_1.objects[-3:]!r}"
            )
            print(msg_info, file=sys.stderr)
            msg_info = "convert txt --> inv"
            print(msg_info, file=sys.stderr)
            lng_cmd_size_after = path_cmp.stat().st_size
            msg_info = f"size (cmp): {lng_cmd_size_after}"
            print(msg_info, file=sys.stderr)
            delta_cmp = lng_cmd_size_after - lng_cmd_size_before
            msg_info = f"delta (cmp): {delta_cmp}"
            print(msg_info, file=sys.stderr)

        #    Compare last commit .inv with updated .inv
        #    If virtual environment not activated, .git/config texconv
        #    executable relative path will not work e.g. sphobjinv-textconv
        #
        #    error: cannot run sphobjinv-textconv: No such file or directory
        #    fatal: unable to read files to diff
        #    exit code 128
        cmp_relpath = misc_info.FNames.INIT + misc_info.Extensions.CMP
        cmd = f"git diff HEAD {cmp_relpath}"
        sp_out = run(cmd, cwd=wd.cwd)
        retcode = sp_out.returncode
        out = sp_out.stdout
        assert retcode == 0
        assert len(out) != 0

        #    On error, not showing locals, so print source file and diff
        if platform.system() in ("Linux", "Windows"):
            print(f"is_file: {Path(cmp_relpath).is_file()}", file=sys.stderr)
            print(f"cmd: {cmd}", file=sys.stderr)
            print(f"diff: {out}", file=sys.stderr)
            print(f"regex: {expected_diff}", file=sys.stderr)

        # Had trouble finding executable's path. On Windows, regex should be OK
        pattern = re.compile(expected_diff)
        lst_matches = pattern.findall(out)
        assert lst_matches is not None
        assert isinstance(lst_matches, list)
        assert len(lst_matches) == 1
