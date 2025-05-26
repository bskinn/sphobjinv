r"""*Direct expect-good API tests for* ``sphobjinv``.

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

import copy
import itertools as itt
import re
from numbers import Number

import dictdiffer
import pytest

import sphobjinv as soi


pytestmark = [pytest.mark.api, pytest.mark.local]


def no_op(val):
    """No-op function to leave Path objects alone in tests."""
    return val


PATH_FXNS = (no_op, str)
PATH_FXN_IDS = ("no_op", "str")


class TestCore:
    """Tests of core sphobjinv functionality."""

    @pytest.mark.parametrize(
        ["actual", "expect"],
        tuple(
            itt.zip_longest(
                soi.SourceTypes,  # actual
                [  # expect
                    soi.SourceTypes.Manual,
                    soi.SourceTypes.BytesPlaintext,
                    soi.SourceTypes.BytesZlib,
                    soi.SourceTypes.FnamePlaintext,
                    soi.SourceTypes.FnameZlib,
                    soi.SourceTypes.DictJSON,
                    soi.SourceTypes.URL,
                ],
                fillvalue=None,
            )
        ),
        ids=(lambda a: a.value if a else a),
    )
    def test_source_types_iteration(self, actual, expect):
        """Confirm that SourceTypes iterates in the expected order."""
        assert actual == expect

    @pytest.mark.parametrize("path_fxn", PATH_FXNS, ids=PATH_FXN_IDS)
    def test_api_compress(self, path_fxn, scratch_path, misc_info, sphinx_load_test):
        """Check that a compress attempt via API throws no errors."""
        src_path = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.DEC)
        dest_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.CMP)

        b_dec = soi.readbytes(path_fxn(src_path))
        b_cmp = soi.compress(b_dec)
        soi.writebytes(path_fxn(dest_path), b_cmp)

        assert dest_path.is_file()

        sphinx_load_test(dest_path)

    @pytest.mark.parametrize("path_fxn", PATH_FXNS, ids=PATH_FXN_IDS)
    def test_api_decompress(self, path_fxn, scratch_path, misc_info, decomp_cmp_test):
        """Check that a decompress attempt via API throws no errors."""
        src_path = scratch_path / (misc_info.FNames.INIT + misc_info.Extensions.CMP)
        dest_path = scratch_path / (misc_info.FNames.MOD + misc_info.Extensions.DEC)

        b_cmp = soi.readbytes(path_fxn(src_path))
        b_dec = soi.decompress(b_cmp)
        soi.writebytes(path_fxn(dest_path), b_dec)

        assert dest_path.is_file()

        decomp_cmp_test(dest_path)

    @pytest.mark.parametrize(
        ["element", "datadict"],
        (
            [
                0,
                {  # attr.Attribute py:class 1 api.html#$ -
                    soi.DataFields.Name: b"attr",
                    soi.DataFields.Domain: b"py",
                    soi.DataFields.Role: b"module",
                    soi.DataFields.Priority: b"0",
                    soi.DataFields.URI: b"index.html#module-$",
                    soi.DataFields.DispName: b"-",
                },
            ],
            [
                -3,
                {  # slots std:label -1 examples.html#$ Slots
                    soi.DataFields.Name: b"validators",
                    soi.DataFields.Domain: b"std",
                    soi.DataFields.Role: b"label",
                    soi.DataFields.Priority: b"-1",
                    soi.DataFields.URI: b"init.html#$",
                    soi.DataFields.DispName: b"Validators",
                },
            ],
        ),
    )
    def test_api_data_regex(self, element, datadict, bytes_txt, misc_info):
        """Confirm the regex for loading data lines is working properly."""
        # Prelim approximate check to be sure we're working with the
        # correct file/data.
        assert len(soi.re.pb_data.findall(bytes_txt)) == 129

        mchs = list(soi.re.pb_data.finditer(bytes_txt))

        assert mchs[element].groupdict() == {_.value: datadict[_] for _ in datadict}

    def test_api_compress_win_eols(self, unix2dos, res_dec):
        """Confirm the scrub for Windows EOLs is working.

        Only a relevant passing test when starting with a decompressed inventory.

        Written based on a surviving mutmut mutant munging the Windows EOL scrub in
        zlib.compress.

        The repeated application of unix2dos tests that the substitution ignores
        existing Windows EOLs in the string.

        """
        b_dec = unix2dos(unix2dos(soi.readbytes(res_dec)))
        b_cmp = soi.compress(b_dec)

        b_dec_new = soi.decompress(b_cmp)

        assert rb"\r\n" not in b_dec_new

    def test_flatdict_schema_valid(self, jsonschema_validator):
        """Confirm that the Inventory JSON schema is itself a valid schema."""
        meta_schema = copy.deepcopy(jsonschema_validator({}).META_SCHEMA)

        # Forbid unrecognized keys
        meta_schema.update({"additionalProperties": False})

        assert jsonschema_validator(meta_schema).is_valid(soi.json_schema)


class TestDataObj:
    """Tests of the DataObj classes."""

    def test_api_dataobjbytes_init(self, bytes_txt):
        """Confirm the DataObjBytes type functions correctly."""
        mch = soi.pb_data.search(bytes_txt)
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_mchdict = {_: b_mchdict[_].decode(encoding="utf-8") for _ in b_mchdict}

        b_dob = soi.DataObjBytes(**b_mchdict)

        s_dob = soi.DataObjBytes(**s_mchdict)

        assert b_dob == s_dob

        assert all(
            getattr(b_dob, _) == getattr(b_dob.as_str, _).encode("utf-8")
            for _ in b_mchdict
        )

    def test_api_dataobjstr_init(self, bytes_txt):
        """Confirm the DataObjStr type functions correctly."""
        mch = soi.pb_data.search(bytes_txt)
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_mchdict = {_: b_mchdict[_].decode(encoding="utf-8") for _ in b_mchdict}

        b_dos = soi.DataObjStr(**b_mchdict)

        s_dos = soi.DataObjStr(**s_mchdict)

        assert b_dos == s_dos

        assert all(
            getattr(s_dos, _) == getattr(b_dos.as_bytes, _).decode("utf-8")
            for _ in s_mchdict
        )

    def test_api_dataobjbytes_flatdictfxn(self, bytes_txt):
        """Confirm that flat dict generating function works."""
        mch = soi.pb_data.search(bytes_txt)

        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        b_jsondict = soi.DataObjBytes(**b_mchdict).json_dict()

        assert b_mchdict == b_jsondict

    def test_api_dataobjstr_flatdictfxn(self, bytes_txt):
        """Confirm that flat dict generating function works."""
        mch = soi.pb_data.search(bytes_txt)

        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_mchdict = {_: b_mchdict[_].decode("utf-8") for _ in b_mchdict}
        s_jsondict = soi.DataObjStr(**b_mchdict).json_dict()

        assert s_mchdict == s_jsondict

    @pytest.mark.parametrize(
        ["dataobjtype", "regex", "lines"],
        (
            [soi.DataObjBytes, soi.pb_data, "byte_lines"],
            [soi.DataObjStr, soi.p_data, "str_lines"],
        ),
        ids=(lambda i: i if isinstance(i, str) else ""),
    )
    @pytest.mark.parametrize("dataline_arg", (True, False))
    @pytest.mark.parametrize("init_expanded", (True, False))
    def test_api_dataobj_datalinefxn(
        self,
        dataobjtype,
        regex,
        lines,
        init_expanded,
        dataline_arg,
        misc_info,
        check,
    ):
        """Confirm that data line formatting function works.

        Test both str and bytes versions of the DataObj.

        Also provides further testing of flat_dict.

        """
        lines_obj = getattr(misc_info, lines)

        dobj = dataobjtype(**regex.search(lines_obj[init_expanded]).groupdict())

        # If dataline_arg is False, should match the value of init_expanded.
        # If dataline_arg is True, should match the True (expanded) value.
        # Thus, the only False (contracted) situation is with both values False.
        dl = dobj.data_line(expand=dataline_arg)
        check.equal(dl, lines_obj[dataline_arg or init_expanded])

        # If dataline_arg is False, should match the value of init_expanded.
        # If dataline_arg is True, should match the False (contracted) value.
        # Thus, the only True (expanded) situation is when init_expanded == True
        # and and dataline_arg == False.
        dl = dobj.data_line(contract=dataline_arg)
        check.equal(dl, lines_obj[init_expanded and not dataline_arg])

    @pytest.mark.parametrize(
        "use_bytes", (True, False), ids=(lambda b: "use_bytes_" + str(b))
    )
    def test_api_dataobj_evolvename(self, use_bytes, res_cmp):
        """Confirm evolving new DataObj instances works properly."""
        inv = soi.Inventory(res_cmp)
        obj = (
            inv.objects[5].as_bytes if use_bytes else inv.objects[5]
        )  # Arbitrary choice
        oldname = obj.name

        newname = b"foo" if use_bytes else "foo"
        obj2 = obj.evolve(name=newname)
        obj3 = obj2.evolve(name=oldname)

        assert obj == obj3
        assert obj2.name == newname

    def test_api_dataobj_equality(self, res_cmp):
        """Confirm various aspects of DataObj equality behavior."""
        inv = soi.Inventory(res_cmp)

        obj1 = inv.objects[0]
        obj2 = inv.objects[1]
        obj3 = obj1.evolve()
        obj4 = obj3.evolve(name="foobar")

        assert obj1 is obj1
        assert obj1 is not obj2
        assert obj1 is not obj3
        assert obj1 is not obj4

        assert obj1 is not obj1.as_bytes
        assert obj1 is obj1.as_bytes.as_str

        assert obj1 == obj1
        assert obj1 != obj2
        assert obj1 == obj3
        assert obj1 != obj4

        assert obj1 != obj1.as_bytes


class TestInventory:
    """Tests of the Inventory class."""

    def test_api_inventory_default_none_instantiation(self, check):
        """Confirm 'manual' instantiation with None."""
        inv = soi.Inventory()

        check.is_none(inv.project)
        check.is_none(inv.version)
        check.equal(inv.count, 0)
        check.is_(inv.source_type, soi.SourceTypes.Manual)

    @pytest.mark.parametrize(
        ["source_type", "inv_arg"],
        [
            (soi.SourceTypes.BytesPlaintext, "plaintext"),
            (soi.SourceTypes.BytesZlib, "zlib"),
            (soi.SourceTypes.FnamePlaintext, "fname_plain"),
            (soi.SourceTypes.FnameZlib, "fname_zlib"),
        ],
        ids=(lambda v: v if isinstance(v, str) else ""),
    )
    @pytest.mark.parametrize("path_fxn", PATH_FXNS, ids=PATH_FXN_IDS)
    def test_api_inventory_bytes_fname_instantiation(
        self,
        source_type,
        inv_arg,
        path_fxn,
        res_path,
        misc_info,
        attrs_inventory_test,
        check,
    ):
        """Check bytes and filename modes for Inventory instantiation."""
        fname = misc_info.FNames.RES

        if source_type in (
            soi.SourceTypes.BytesPlaintext,
            soi.SourceTypes.FnamePlaintext,
        ):
            fname += misc_info.Extensions.DEC
        else:
            fname += misc_info.Extensions.CMP

        source = path_fxn(res_path / fname)

        if source_type in (soi.SourceTypes.BytesPlaintext, soi.SourceTypes.BytesZlib):
            # Passing in the actual inventory contents, and not just the location
            source = soi.readbytes(source)

        # General import, without a specified kwarg
        with check(msg="general"):
            attrs_inventory_test(soi.Inventory(source), source_type)

        # Importing with the respective kwarg for each source type
        with check(msg="specific"):
            inv = soi.Inventory(**{inv_arg: source})
            attrs_inventory_test(inv, source_type)

        # Special case for plaintext bytes, try decoding it
        if source_type is soi.SourceTypes.BytesPlaintext:
            with check(msg="plaintext_bytes"):
                inv = soi.Inventory(**{inv_arg: source.decode("utf-8")})
                attrs_inventory_test(inv, source_type)

    def test_api_inventory_equality(self, res_cmp):
        """Confirm the attrs Inventory equality methods work as expected."""
        inv1 = soi.Inventory(res_cmp)
        inv2 = soi.Inventory(res_cmp)
        inv3 = soi.Inventory(inv1.data_file())
        inv4 = soi.Inventory(res_cmp)

        assert inv1 is inv1
        assert inv1 is not inv2
        assert inv1 is not inv3

        assert inv1 == inv1
        assert inv1 == inv2
        assert inv1 == inv3

        inv2.objects[0].name = "foobar"
        inv3.project = "quux"
        inv4.version = "0.0"

        assert inv1 != inv2
        assert inv1 != inv3
        assert inv1 != inv4

    @pytest.mark.parametrize("prop", ("none", "expand", "contract"))
    def test_api_inventory_flatdict_jsonvalidate(
        self, prop, res_cmp, jsonschema_validator
    ):
        """Confirm that the flat_dict properties generated valid JSON."""
        inv = soi.Inventory(res_cmp)
        val = jsonschema_validator(soi.json_schema)

        kwarg = {} if prop == "none" else {prop: True}

        val.validate(inv.json_dict(**kwarg))

    def test_api_inventory_flatdict_reimport(self, res_dec, attrs_inventory_test):
        """Confirm re-import of a generated flat_dict."""
        inv = soi.Inventory(res_dec)
        inv = soi.Inventory(inv.json_dict())

        attrs_inventory_test(inv, soi.SourceTypes.DictJSON)

    @pytest.mark.parametrize(
        "metadata",
        ["test string", {"this": "foo", "that": "bar"}, 42],
        ids=(lambda v: re.search("'([^']+)'", str(type(v))).group(1)),
    )
    def test_api_inventory_flatdict_reimportwithmetadata(
        self, metadata, res_dec, attrs_inventory_test
    ):
        """Confirm re-import of a generated flat_dict with metadata."""
        inv = soi.Inventory(res_dec)
        d = inv.json_dict()

        d.update({"metadata": metadata})

        inv = soi.Inventory(d)

        attrs_inventory_test(inv, soi.SourceTypes.DictJSON)

    def test_api_inventory_toosmallflatdict_importbutignore(self, res_dec):
        """Confirm no error when flat dict passed w/too few objs w/ignore."""
        inv = soi.Inventory(res_dec)
        d = inv.json_dict()
        d.pop("12")

        inv2 = soi.Inventory(d, count_error=False)

        # 128 (one less than 129) b/c the loop continues past missing elements
        assert inv2.count == 128

    def test_api_inventory_namesuggest(self, res_cmp, check):
        """Confirm object name suggestion is nominally working on a specific object."""
        rst = ":py:function:`attr.attr.evolve`"
        idx = 10

        inv = soi.Inventory(str(res_cmp))

        # No test on the exact fuzzywuzzy match score in these since
        # it could change as fw continues development
        check.equal(inv.suggest("evolve")[0], rst)

        check.equal(inv.suggest("evolve", with_index=True)[0], (rst, idx))

        rec = inv.suggest("evolve", with_score=True)
        check.equal(rec[0][0], rst)
        check.is_instance(rec[0][1], Number)

        rec = inv.suggest("evolve", with_index=True, with_score=True)
        check.equal(rec[0][0], rst)
        check.is_instance(rec[0][1], Number)
        check.equal(rec[0][2], idx)

    @pytest.mark.testall
    def test_api_inventory_suggest_operation(self, testall_inv_path):
        """Confirm that a suggest operation works on all smoke-test inventories."""
        inv = soi.Inventory(testall_inv_path)

        inv.suggest("class")

    @pytest.mark.testall
    def test_api_inventory_datafile_gen_and_reimport(
        self,
        testall_inv_path,
        res_path,
        scratch_path,
        misc_info,
        sphinx_load_test,
        pytestconfig,
    ):
        """Confirm integrated data_file export/import behavior."""
        fname = testall_inv_path.name
        scr_fpath = scratch_path / fname

        # Drop most unless testall
        if not pytestconfig.getoption("--testall") and fname != "objects_attrs.inv":
            pytest.skip("'--testall' not specified")

        # Make Inventory
        inv1 = soi.Inventory(str(res_path / fname))

        # Generate new zlib file and reimport
        data = inv1.data_file()
        cmp_data = soi.compress(data)
        soi.writebytes(str(scr_fpath), cmp_data)
        inv2 = soi.Inventory(str(scr_fpath))

        # Test the things
        assert inv1 == inv2

        # Ensure sphinx likes the regenerated inventory
        sphinx_load_test(scr_fpath)

    @pytest.mark.testall
    def test_api_inventory_matches_sphinx_ifile(
        self,
        testall_inv_path,
        scratch_path,
        misc_info,
        pytestconfig,
        sphinx_ifile_load,
        sphinx_ifile_data_count,
        sphinx_version,
    ):
        """Confirm no-op per Sphinx on passing through sphobjinv.Inventory."""
        fname = testall_inv_path.name
        scr_fpath = scratch_path / fname

        # Drop most unless testall
        if not pytestconfig.getoption("--testall") and fname != "objects_attrs.inv":
            pytest.skip("'--testall' not specified")

        original_ifile_data = sphinx_ifile_load(testall_inv_path)

        inv = soi.Inventory(testall_inv_path)
        soi.writebytes(scr_fpath, soi.compress(inv.data_file()))
        soi_ifile_data = sphinx_ifile_load(scr_fpath)

        assert not list(dictdiffer.diff(soi_ifile_data, original_ifile_data)), fname

        if "celery" in fname:  # pragma: no cover
            # Celery inventory contains some exact domain:role:name duplicates
            assert inv.count == 54 + sphinx_ifile_data_count(original_ifile_data), fname

        elif "opencv" in fname:  # pragma: no cover
            # OpenCV inventory contains some lines that
            # parse incorrectly after sphinx/#8225, which was first
            # incorporated into Sphinx 3.3.0
            if sphinx_version < (3, 3, 0):
                assert inv.count == sphinx_ifile_data_count(original_ifile_data), fname
            else:
                assert inv.count == 13 + sphinx_ifile_data_count(
                    original_ifile_data
                ), fname

        elif "jsonschema" in fname:  # pragma: no cover
            # The version of the jsonschema inventory held in tests/resource
            # has an item with an empty uri. Sphinx<2.4 does not import this line
            # correctly.
            if sphinx_version < (2, 4, 0):
                assert inv.count == 1 + sphinx_ifile_data_count(
                    original_ifile_data
                ), fname
            else:
                assert inv.count == sphinx_ifile_data_count(original_ifile_data), fname

        elif "fonttools" in fname:  # pragma: no cover
            # One object appears to have a misbehaving character that Sphinx
            # rejects on an attempted import in ~recent versions
            if sphinx_version < (3, 3, 0):
                assert inv.count == sphinx_ifile_data_count(original_ifile_data), fname
            else:
                assert inv.count == 1 + sphinx_ifile_data_count(
                    original_ifile_data
                ), fname

        elif "django.inv" in fname:  # pragma: no cover
            # 13 objects misbehave on import for Sphinx >= 3.3.0
            if sphinx_version < (3, 3, 0):
                assert inv.count == sphinx_ifile_data_count(original_ifile_data), fname
            else:
                assert inv.count == 13 + sphinx_ifile_data_count(
                    original_ifile_data
                ), fname

        elif "sphinx.inv" in fname:  # pragma: no cover
            assert inv.count == 4 + sphinx_ifile_data_count(original_ifile_data), fname

        else:
            assert inv.count == sphinx_ifile_data_count(original_ifile_data), fname

    def test_api_inventory_one_object_flatdict(self):
        """Confirm a flat dict inventory with one object imports ok.

        Addresses edge case identified via mutation testing.

        """
        inv = soi.Inventory()
        inv.project = "Foo"
        inv.version = "1.2"
        inv.objects.append(
            soi.DataObjStr(
                name="bar",
                domain="py",
                role="function",
                priority="1",
                uri="$",
                dispname="-",
            )
        )

        # Should not raise an exception; assert is to emphasize this is the check
        assert soi.Inventory(inv.json_dict())
