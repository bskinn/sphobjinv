r"""*Textconv CLI tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    22 Dec 2025

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

import shlex
import subprocess as sp  # noqa: S404
from pathlib import Path

import pytest
from stdio_mgr import stdio_mgr

from sphobjinv import Inventory
from tests.enum import CLICommand


CLI_TEST_TIMEOUT = 2
CLI_CMDS = ["sphobjinv-textconv"]

pytestmark = [pytest.mark.cli, pytest.mark.textconv, pytest.mark.local]


class TestMisc:
    """Tests for miscellaneous CLI functions."""

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    @pytest.mark.parametrize("cmd", CLI_CMDS)
    def test_cli_invocations(self, cmd):
        """Confirm that actual shell invocations do not error."""
        runargs = shlex.split(cmd)
        runargs.append("--help")

        out = sp.check_output(" ".join(runargs), shell=True).decode()  # noqa: S602

        assert "sphobjinv" in out
        assert "infile" in out

    # @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    # def test_cli_version_exits_ok(self, run_cmdline_test):
    #     """Confirm --version exits cleanly."""
    #     run_cmdline_test(["-v"])

    # @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    # def test_cli_noargs_shows_help(self, run_cmdline_test):
    #     """Confirm help shown when invoked with no arguments."""
    #     with stdio_mgr() as (in_, out_, err_):
    #         run_cmdline_test([])

    #         assert "usage: sphobjinv" in out_.getvalue()

    # @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    # def test_cli_no_subparser_prs_exit(self, run_cmdline_test):
    #     """Confirm exit code 2 if option passed but no subparser provided."""
    #     with stdio_mgr() as (in_, out_, err_):
    #         run_cmdline_test(["--foo"], expect=2)

    #         assert "error: No subparser selected" in err_.getvalue()

    # @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    # def test_cli_bad_subparser_prs_exit(self, run_cmdline_test):
    #     """Confirm exit code 2 if invalid subparser provided."""
    #     with stdio_mgr() as (in_, out_, err_):
    #         run_cmdline_test(["foo"], expect=2)

    #         assert "invalid choice: 'foo'" in err_.getvalue()


# class TestConvertGood:
#     """Tests for expected-good convert functionality."""

#     @pytest.mark.parametrize(
#         ["out_ext", "cli_arg"],
#         [(".txt", "plain"), (".inv", "zlib"), (".json", "json")],
#         ids=(lambda i: "" if i.startswith(".") else i),
#     )
#     @pytest.mark.parametrize(
#         "in_ext", [".txt", ".inv", ".json"], ids=(lambda i: i.split(".")[-1])
#     )
#     @pytest.mark.timeout(CLI_TEST_TIMEOUT)
#     def test_cli_convert_default_outname(
#         self,
#         in_ext,
#         out_ext,
#         cli_arg,
#         scratch_path,
#         run_cmdline_test,
#         decomp_cmp_test,
#         sphinx_load_test,
#         misc_info,
#     ):
#         """Confirm cmdline conversions with only input file arg."""
#         if in_ext == out_ext:
#             pytest.skip("Ignore no-change conversions")

#         src_path = scratch_path / (misc_info.FNames.INIT + in_ext)
#         dest_path = scratch_path / (misc_info.FNames.INIT + out_ext)

#         assert src_path.is_file()
#         assert dest_path.is_file()

#         dest_path.unlink()

#         cli_arglist = ["convert", cli_arg, str(src_path)]
#         run_cmdline_test(cli_arglist)
#         assert dest_path.is_file()

#         if cli_arg == "zlib":
#             sphinx_load_test(dest_path)
#         if cli_arg == "plain":
#             decomp_cmp_test(dest_path)

#     @pytest.mark.timeout(CLI_TEST_TIMEOUT * 2)
#     def test_cli_convert_expandcontract(
#         self, scratch_path, misc_info, run_cmdline_test
#     ):
#         """Confirm cmdline contract decompress of zlib with input file arg."""
#         cmp_path = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.CMP)
#         dec_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.DEC)
#         recmp_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.CMP)

#         run_cmdline_test(["convert", "plain", "-e", str(cmp_path), str(dec_path)])
#         assert dec_path.is_file()

#         run_cmdline_test(["convert", "zlib", "-c", str(dec_path), str(recmp_path)])
#         assert recmp_path.is_file()

#     @pytest.mark.parametrize(
#         "dst_name", [True, False], ids=(lambda v: "dst_name" if v else "no_dst_name")
#     )
#     @pytest.mark.parametrize(
#         "dst_path", [True, False], ids=(lambda v: "dst_path" if v else "no_dst_path")
#     )
#     @pytest.mark.parametrize(
#         "src_path", [True, False], ids=(lambda v: "src_path" if v else "no_src_path")
#     )
#     @pytest.mark.timeout(CLI_TEST_TIMEOUT)
#     def test_cli_convert_various_pathargs(
#         self,
#         src_path,
#         dst_path,
#         dst_name,
#         scratch_path,
#         misc_info,
#         run_cmdline_test,
#         decomp_cmp_test,
#         monkeypatch,
#     ):
#         """Confirm the various src/dest path/file combinations work."""
#         init_dst_fname = misc_info.FNames.INIT + misc_info.Extensions.DEC
#         mod_dst_fname = misc_info.FNames.MOD + misc_info.Extensions.DEC

#         src_path = (scratch_path.resolve() if src_path else Path(".")) / (
#             misc_info.FNames.INIT + misc_info.Extensions.CMP
#         )
#         dst_path = (scratch_path.resolve() if dst_path else Path(".")) / (
#             mod_dst_fname if dst_name else ""
#         )

#         full_dst_path = scratch_path.resolve() / (
#             mod_dst_fname if dst_name else init_dst_fname
#         )

#         assert (scratch_path / init_dst_fname).is_file()
#         (scratch_path / init_dst_fname).unlink()

#         with monkeypatch.context() as m:
#             m.chdir(scratch_path)
#             run_cmdline_test(["convert", "plain", str(src_path), str(dst_path)])
#             assert full_dst_path.is_file()

#         decomp_cmp_test(full_dst_path)

#     @pytest.mark.timeout(CLI_TEST_TIMEOUT * 50 * 3)
#     @pytest.mark.testall
#     def test_cli_convert_cycle_formats(
#         self,
#         testall_inv_path,
#         res_path,
#         scratch_path,
#         run_cmdline_test,
#         misc_info,
#         pytestconfig,
#         check,
#     ):
#         """Confirm conversion in a loop, reading/writing all formats."""
#         res_src_path = res_path / testall_inv_path
#         plain_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.DEC)
#         json_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.JSON)
#         zlib_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.CMP)

#         if (
#             not pytestconfig.getoption("--testall")
#             and testall_inv_path.name != "objects_attrs.inv"
#         ):
#             pytest.skip("'--testall' not specified")

#         run_cmdline_test(["convert", "plain", str(res_src_path), str(plain_path)])
#         run_cmdline_test(["convert", "json", str(plain_path), str(json_path)])
#         run_cmdline_test(["convert", "zlib", str(json_path), str(zlib_path)])

#         invs = {
#             "orig": Inventory(str(res_src_path)),
#             "plain": Inventory(str(plain_path)),
#             "zlib": Inventory(str(zlib_path)),
#             "json": Inventory(json.loads(json_path.read_text())),
#         }

#         for fmt, attrib in product(
#             ("plain", "zlib", "json"),
#             (
#                 HeaderFields.Project.value,
#                 HeaderFields.Version.value,
#                 HeaderFields.Count.value,
#             ),
#         ):
#             check.equal(getattr(invs[fmt], attrib), getattr(invs["orig"], attrib))

#     @pytest.mark.timeout(CLI_TEST_TIMEOUT)
#     def test_cli_overwrite_prompt_and_behavior(
#         self, res_path, scratch_path, misc_info, run_cmdline_test
#     ):
#         """Confirm overwrite prompt works properly."""
#         src_path_1 = res_path / "objects_attrs.inv"
#         src_path_2 = res_path / "objects_sarge.inv"
#         dst_path = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.DEC)
#         dst_path.unlink()

#         args = ["convert", "plain", None, str(dst_path)]

#         # Initial decompress
#         args[2] = str(src_path_1)
#         with stdio_mgr() as (in_, out_, err_):
#             run_cmdline_test(args)

#             assert "converted" in err_.getvalue()
#             assert "(plain)" in err_.getvalue()

#         # First overwrite, declining clobber
#         args[2] = str(src_path_2)
#         with stdio_mgr("n\n") as (in_, out_, err_):
#             run_cmdline_test(args)

#             assert "(Y/N)? n" in out_.getvalue()

#         assert "attrs" == Inventory(str(dst_path)).project

#         # Second overwrite, with clobber
#         with stdio_mgr("y\n") as (in_, out_, err_):
#             run_cmdline_test(args)

#             assert "(Y/N)? y" in out_.getvalue()

#         assert "Sarge" == Inventory(str(dst_path)).project

#     def test_cli_stdin_clobber(
#         self, res_path, scratch_path, misc_info, run_cmdline_test
#     ):
#         """Confirm clobber with stdin data only with --overwrite."""
#         src_path_sarge = res_path / "objects_sarge.inv"
#         dst_path = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.CMP)

#         assert "attrs" == Inventory(dst_path).project

#         data = json.dumps(Inventory(src_path_sarge).json_dict())

#         args = ["convert", "plain", "-", str(dst_path)]
#         with stdio_mgr(data):
#             run_cmdline_test(args)
#         assert "attrs" == Inventory(dst_path).project

#         args.append("-o")
#         with stdio_mgr(data):
#             run_cmdline_test(args)
#         assert "Sarge" == Inventory(dst_path).project

#     def test_cli_json_no_metadata_url(
#         self, res_cmp, scratch_path, misc_info, run_cmdline_test
#     ):
#         """Confim JSON generated from local inventory has no url in metadata."""
#         json_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.JSON)

#         run_cmdline_test(
#             ["convert", "json", str(res_cmp.resolve()), str(json_path.resolve())]
#         )

#         d = json.loads(json_path.read_text())

#         assert "url" not in d.get("metadata", {})

#     def test_cli_json_export_import(
#         self, res_cmp, scratch_path, misc_info, run_cmdline_test, sphinx_load_test
#     ):
#         """Confirm JSON sent to stdout from local source imports ok."""
#         mod_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.CMP)

#         with stdio_mgr() as (in_, out_, err_):
#             run_cmdline_test(["convert", "json", str(res_cmp.resolve()), "-"])

#             data = out_.getvalue()

#         with stdio_mgr(data) as (in_, out_, err_):
#             run_cmdline_test(["convert", "zlib", "-", str(mod_path.resolve())])

#         assert Inventory(json.loads(data))
#         assert Inventory(mod_path)
#         sphinx_load_test(mod_path)


class TestFail:
    """Tests for expected-fail behaviors."""

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_wrongfiletype(
        self, scratch_path, run_cmdline_test, monkeypatch
    ):
        """Confirm exit code 1 with invalid file format."""
        monkeypatch.chdir(scratch_path)
        fname = "testfile"
        Path(fname).write_bytes(b"this is not objects.inv\n")

        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test([fname], command=CLICommand.Textconv, expect=1)
            assert "Unrecognized" in err_.getvalue()

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_missingfile(self, run_cmdline_test):
        """Confirm exit code 1 with nonexistent file specified."""
        run_cmdline_test(
            ["thisfileshouldbeabsent.txt"], command=CLICommand.Textconv, expect=1
        )

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_outputdir_provided(
        self, res_cmp, scratch_path, run_cmdline_test
    ):
        """Confirm exit code 2 when too many inputs are provided."""
        run_cmdline_test(
            [
                res_cmp,
                str(scratch_path / "objects.txt"),
            ],
            command=CLICommand.Textconv,
            expect=2,
        )

    @pytest.mark.timeout(CLI_TEST_TIMEOUT)
    def test_clifail_convert_pathonlysrc(self, scratch_path, run_cmdline_test):
        """Confirm cmdline plaintext convert with input directory arg fails."""
        run_cmdline_test(
            [str(scratch_path)],
            command=CLICommand.Textconv,
            expect=1,
        )

    def test_clifail_no_url_arg(self, run_cmdline_test):
        """Confirm textconv parser errors on non-existent -u flag."""
        with stdio_mgr() as (in_, out_, err_):
            run_cmdline_test(
                ["-u", "nofile.inv"], command=CLICommand.Textconv, expect=2
            )
            assert "unrecognized argument" in err_.getvalue()


class TestStdio:
    """Tests for the stdin/stdout functionality."""

    def test_cli_stdio_output(self, res_cmp, run_cmdline_test):
        """Confirm that inventory data can be written to stdout."""
        with stdio_mgr() as (_, out_, _):
            run_cmdline_test([str(res_cmp.resolve())], command=CLICommand.Textconv)

            result = out_.getvalue()

        inv1 = Inventory(res_cmp)
        inv2 = Inventory(result.encode("utf-8"))

        assert inv1 == inv2
