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
import re
import sys
from pathlib import Path

from sphobjinv import DataObjStr
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
        # word placeholder --> \w+
        # Escape $ --> \$
        # Escape + --> \+
        expected_diff = (
            r"^diff --git a/objects.inv b/objects.inv\n"
            r"index \w+..\w+ \w+\n"
            r"--- a/objects.inv\n"
            r"\+\+\+ b/objects.inv\n"
            r"@@ -131,4 \+131,5 @@ types std:doc -1 types.html Type Annotations\n"
            r" validators std:label -1 init.html#\$ Validators\n"
            r" version-info std:label -1 api.html#\$ -\n"
            r" why std:doc -1 why.html Why not…\n"
            r"\+attrs.validators.set_cheat_mode py:function 1 api.html#\$ -\n"
            r" \n$"
        )

        # prepare
        #    project folder
        path_cwd = scratch_path
        wd = WorkDir(path_cwd)

        path_soi = Path(sys.executable).parent.joinpath("sphobjinv")
        soi_path = str(path_soi)
        path_soi_textconv = Path(sys.executable).parent.joinpath("sphobjinv-textconv")

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
        lines = [
            """[diff "inv"]""",
            f"""	textconv = {path_soi_textconv!s}\n""",
        ]
        gc_textconv = "\n".join(lines)
        str_git_config = f"{str_git_config}\n{gc_textconv}\n"
        path_git_config.write_text(str_git_config)

        #    .gitattributes
        #    Informs git: .inv are binary files and which cmd converts .inv --> .txt
        path_ga = path_cwd / ".gitattributes"
        path_ga.touch()
        str_gitattributes = path_ga.read_text()
        ga_textconv = "*.inv binary diff=inv"
        str_gitattributes = f"{str_gitattributes}\n{ga_textconv}"
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

        #    plain --> zlib
        cmd = f"{soi_path} convert -q zlib {dst_dec_path} {dst_cmp_path}"
        wd(cmd)

        #    Compare last commit .inv with updated .inv
        cmd = f"git diff HEAD {misc_info.FNames.INIT + misc_info.Extensions.CMP}"
        sp_out = run(cmd, cwd=wd.cwd)
        retcode = sp_out.returncode
        out = sp_out.stdout
        assert retcode == 0
        pattern = re.compile(expected_diff)
        lst_matches = pattern.findall(out)
        assert lst_matches is not None
        assert isinstance(lst_matches, list)
        assert len(lst_matches) == 1