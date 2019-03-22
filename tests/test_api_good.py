r"""*Direct expect-good API tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    20 Mar 2019

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

import unittest as ut

from .sphobjinv_base import B_LINES_0, S_LINES_0
from .sphobjinv_base import DEC_EXT, CMP_EXT
from .sphobjinv_base import INIT_FNAME_BASE, MOD_FNAME_BASE
from .sphobjinv_base import RES_FNAME_BASE, INVALID_FNAME
from .sphobjinv_base import REMOTE_URL, P_INV, TESTALL
from .sphobjinv_base import SuperSphobjinv
from .sphobjinv_base import copy_dec, copy_cmp, scr_path, res_path
from .sphobjinv_base import decomp_cmp_test, file_exists_test
from .sphobjinv_base import sphinx_load_test


import itertools as itt

import pytest

import sphobjinv as soi


pytestmark = [pytest.mark.api, pytest.mark.good, pytest.mark.local]


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
def test_source_types_iteration(actual, expect):
    """Confirm that SourceTypes iterates in the expected order."""
    assert actual.value == expect.value


def test_api_compress(scratch_path, misc_info, sphinx_load_test):
    """Check that a compress attempt via API throws no errors."""

    src_path = scratch_path / (
        misc_info.FNames.INIT_FNAME_BASE.value
        + misc_info.Extensions.DEC_EXT.value
    )
    dest_path = scratch_path / (
        misc_info.FNames.MOD_FNAME_BASE.value
        + misc_info.Extensions.CMP_EXT.value
    )

    try:
        b_dec = soi.readbytes(str(src_path))
        b_cmp = soi.compress(b_dec)
        soi.writebytes(str(dest_path), b_cmp)
    except Exception as e:
        pytest.fail("objects.txt compression failed.")

    assert dest_path.is_file()

    sphinx_load_test(dest_path)


def test_api_decompress(scratch_path, misc_info, decomp_cmp_test):
    """Check that a decompress attempt via API throws no errors."""

    src_path = scratch_path / (
        misc_info.FNames.INIT_FNAME_BASE.value
        + misc_info.Extensions.CMP_EXT.value
    )
    dest_path = scratch_path / (
        misc_info.FNames.MOD_FNAME_BASE.value
        + misc_info.Extensions.DEC_EXT.value
    )

    try:
        b_cmp = soi.readbytes(str(src_path))
        b_dec = soi.decompress(b_cmp)
        soi.writebytes(str(dest_path), b_dec)
    except Exception as e:
        pytest.fail("objects.inv decompression failed.")

    assert dest_path.is_file()

    decomp_cmp_test(dest_path)


@pytest.mark.parametrize(
    ["element", "datadict"],
    (
        [
            0,
            {  # attr.Attribute py:class 1 api.html#$ -
                soi.DataFields.Name: b"attr.Attribute",
                soi.DataFields.Domain: b"py",
                soi.DataFields.Role: b"class",
                soi.DataFields.Priority: b"1",
                soi.DataFields.URI: b"api.html#$",
                soi.DataFields.DispName: b"-",
            },
        ],
        [
            -3,
            {  # slots std:label -1 examples.html#$ Slots
                soi.DataFields.Name: b"slots",
                soi.DataFields.Domain: b"std",
                soi.DataFields.Role: b"label",
                soi.DataFields.Priority: b"-1",
                soi.DataFields.URI: b"examples.html#$",
                soi.DataFields.DispName: b"Slots",
            },
        ],
    ),
)
def test_api_data_regex(element, datadict, bytes_txt, misc_info):
    """Confirm the regex for loading data lines is working properly."""
    import sphobjinv as soi

    # Prelim approximate check to be sure we're working with the
    # correct file/data.
    assert len(soi.re.pb_data.findall(bytes_txt)) == 56

    mchs = list(soi.re.pb_data.finditer(bytes_txt))

    assert mchs[element].groupdict() == {
        _.value: datadict[_] for _ in datadict
    }


@pytest.mark.xfail(
    reason="Will fail until .as_xxx properties are removed from attrs cmp"
)
def test_api_dataobjbytes_init(bytes_txt):
    """Confirm the DataObjBytes type functions correctly."""

    mch = soi.pb_data.search(bytes_txt)
    b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
    s_mchdict = {_: b_mchdict[_].decode(encoding="utf-8") for _ in b_mchdict}

    try:
        b_dob = soi.DataObjBytes(**b_mchdict)
    except Exception:
        pytest.fail("bytes instantiation failed")

    try:
        s_dob = soi.DataObjBytes(**s_mchdict)
    except Exception:
        pytest.fail("str instantiation failed")

    assert b_dob == s_dob

    assert all(
        [
            getattr(b_dob, _) == getattr(b_dob.as_str, _).encode("utf-8")
            for _ in b_mchdict
        ]
    )


@pytest.mark.xfail(
    reason="Will fail until .as_xxx properties are removed from attrs cmp"
)
def test_api_dataobjstr_init(bytes_txt):
    """Confirm the DataObjStr type functions correctly."""

    mch = soi.pb_data.search(bytes_txt)
    b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
    s_mchdict = {_: b_mchdict[_].decode(encoding="utf-8") for _ in b_mchdict}

    try:
        b_dos = soi.DataObjStr(**b_mchdict)
    except Exception:
        pytest.fail("bytes instantiation failed")

    try:
        s_dos = soi.DataObjStr(**s_mchdict)
    except Exception:
        pytest.fail("str instantiation failed")

    assert b_do == s_dos

    assert all(
        [
            getattr(s_dos, _) == getattr(s_dob.as_bytes, _).decode("utf-8")
            for _ in s_mchdict
        ]
    )


@pytest.mark.skip(reason="Un-converted tests")
class TestSphobjinvAPIExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_API_DataObjStr_InitCheck(self):
        """Confirm the DataObjStr type functions correctly."""
        import sphobjinv as soi

        # Pull .txt file and match first data line
        b_dec = soi.readbytes(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_mchdict = {
            _: b_mchdict[_].decode(encoding="utf-8") for _ in b_mchdict
        }

        # Confirm DataObjStr instantiates w/bytes
        with self.subTest("inst_bytes"):
            try:
                b_dos = soi.DataObjStr(**b_mchdict)
            except Exception:
                self.fail("bytes instantiation failed")

        # Confirm DataObjStr instantiates w/str
        with self.subTest("inst_str"):
            try:
                s_dos = soi.DataObjStr(**s_mchdict)
            except Exception:
                self.fail("str instantiation failed")

        # Confirm members match
        for _ in s_mchdict:
            with self.subTest("match_" + _):
                self.assertEqual(getattr(b_dos, _), getattr(s_dos, _))

        # Confirm bytes-equivalents match
        for _ in s_mchdict:
            with self.subTest("str_equiv_" + _):
                self.assertEqual(
                    getattr(s_dos, _),
                    getattr(s_dos.as_bytes, _).decode(encoding="utf-8"),
                )

    def test_API_DataObjBytes_FlatDictFxn(self):
        """Confirm that flat dict generating function works."""
        import sphobjinv as soi

        # Pull .txt file and match first data line
        b_dec = soi.readbytes(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)

        # Extract the match information, stuff into a DataObjBytes
        # instance, and extract the flat_dict
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        b_jsondict = soi.DataObjBytes(**b_mchdict).json_dict()

        # Check matchingness
        for _ in b_mchdict:
            with self.subTest(_):
                self.assertEqual(b_mchdict[_], b_jsondict[_])

    def test_API_DataObjStr_FlatDictFxn(self):
        """Confirm that flat dict generating function works."""
        import sphobjinv as soi

        # Pull .txt file and match first data line
        b_dec = soi.readbytes(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)

        # Extract the match information, stuff into a DataObjStr
        # instance, and extract the flat_dict
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_jsondict = soi.DataObjStr(**b_mchdict).json_dict()

        # Check matchingness
        for _ in b_mchdict:
            with self.subTest(_):
                self.assertEqual(
                    b_mchdict[_].decode(encoding="utf-8"), s_jsondict[_]
                )

    # These methods testing data_line also implicitly test flat_dict
    def test_API_DataObjBytes_DataLineFxn(self):
        """Confirm that data line formatting function works."""
        from itertools import product

        import sphobjinv as soi

        # Generate and check data line as bytes, both expanded
        # and contracted, with both expanded/contracted flag
        for _, __ in product(B_LINES_0, repeat=2):  # True/False product
            dob = soi.DataObjBytes(
                **soi.pb_data.search(B_LINES_0[_]).groupdict()
            )
            b_dl = dob.data_line(expand=__)
            with self.subTest(str(_) + "_expand_" + str(__)):
                self.assertEqual(b_dl, B_LINES_0[_ or __])

            b_dl = dob.data_line(contract=__)
            with self.subTest(str(_) + "_contract_" + str(__)):
                self.assertEqual(b_dl, B_LINES_0[_ and not __])

    def test_API_DataObjStr_DataLineFxn(self):
        """Confirm that data line formatting function works."""
        from itertools import product

        import sphobjinv as soi

        # Generate and check data line as str, both expanded
        # and contracted, with both expanded/contracted flag
        for _, __ in product(S_LINES_0, repeat=2):  # True/False product
            dos = soi.DataObjStr(**soi.p_data.search(S_LINES_0[_]).groupdict())
            s_dl = dos.data_line(expand=__)
            with self.subTest(str(_) + "_expand_" + str(__)):
                self.assertEqual(s_dl, S_LINES_0[_ or __])

    def test_API_DataObjStr_EvolveName(self):
        """Confirm evolving a new |str| instance works properly."""
        from sphobjinv import Inventory as Inv

        inv = Inv(res_path(RES_FNAME_BASE + CMP_EXT))
        obj = inv.objects[5]

        newname = "foo"
        obj2 = obj.evolve(name=newname)

        for k in obj.json_dict():
            with self.subTest(k):
                if k == "name":
                    self.assertEqual(obj2.name, newname)
                else:
                    self.assertEqual(getattr(obj, k), getattr(obj2, k))

    def test_API_DataObjBytes_EvolveName(self):
        """Confirm evolving a new |bytes| instance works properly."""
        from sphobjinv import Inventory as Inv

        inv = Inv(res_path(RES_FNAME_BASE + CMP_EXT))
        obj = inv.objects[5].as_bytes

        newname = b"foo"
        obj2 = obj.evolve(name=newname)

        for k in obj.json_dict():
            with self.subTest(k):
                if k == "name":
                    self.assertEqual(obj2.name, newname)
                else:
                    self.assertEqual(getattr(obj, k), getattr(obj2, k))


@pytest.mark.skip("Un-converted tests")
class TestSphobjinvAPIInventoryExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing Inventory code accuracy w/good params & expected behavior."""

    def test_API_Inventory_DefaultNoneInstantiation(self):
        """Confirm 'manual' instantiation with None."""
        import sphobjinv as soi

        inv = soi.Inventory()

        with self.subTest("project"):
            self.assertEqual(inv.project, None)

        with self.subTest("version"):
            self.assertEqual(inv.version, None)

        with self.subTest("count"):
            self.assertEqual(inv.count, 0)

        with self.subTest("source_type"):
            self.assertEqual(inv.source_type, soi.SourceTypes.Manual)

    def check_attrs_inventory(self, inv, st, subtest_id):
        """Encapsulate high-level consistency tests for Inventory objects."""
        with self.subTest("{0}_{1}_project".format(subtest_id, st.value)):
            self.assertEqual(inv.project, "attrs")

        with self.subTest("{0}_{1}_version".format(subtest_id, st.value)):
            self.assertEqual(inv.version, "17.2")

        with self.subTest("{0}_{1}_count".format(subtest_id, st.value)):
            self.assertEqual(inv.count, 56)

        with self.subTest("{0}_{1}_source_type".format(subtest_id, st.value)):
            self.assertEqual(inv.source_type, st)

    def test_API_Inventory_TestMostImports(self):
        """Check all high-level modes for Inventory instantiation."""
        from sphobjinv import readbytes, Inventory as Inv, SourceTypes as ST
        from sphobjinv.data import _utf8_decode

        sources = {
            ST.BytesPlaintext: readbytes(res_path(RES_FNAME_BASE + DEC_EXT)),
            ST.BytesZlib: readbytes(res_path(RES_FNAME_BASE + CMP_EXT)),
            ST.FnamePlaintext: res_path(RES_FNAME_BASE + DEC_EXT),
            ST.FnameZlib: res_path(RES_FNAME_BASE + CMP_EXT),
        }

        for st in ST:
            if st in [ST.Manual, ST.DictJSON, ST.URL]:
                # Manual isn't tested
                # DictJSON is tested independently, to avoid crashing this
                #  test if something goes wrong in the generation & reimport.
                # URL is its own beast, tested in the separate Nonlocal
                #  class, below.
                continue

            self.check_attrs_inventory(Inv(sources[st]), st, "general")

            if st == ST.BytesPlaintext:
                inv = Inv(plaintext=sources[st])
                self.check_attrs_inventory(inv, st, st.value)

                inv = Inv(plaintext=_utf8_decode(sources[st]))
                self.check_attrs_inventory(inv, st, st.value)

            if st == ST.BytesZlib:
                inv = Inv(zlib=sources[st])
                self.check_attrs_inventory(inv, st, st.value)

            if st == ST.FnamePlaintext:
                inv = Inv(fname_plain=sources[st])
                self.check_attrs_inventory(inv, st, st.value)

            if st == ST.FnameZlib:
                inv = Inv(fname_zlib=sources[st])
                self.check_attrs_inventory(inv, st, st.value)

    def test_API_Inventory_FlatDictJSONValidate(self):
        """Confirm that the flat_dict properties generated valid JSON."""
        import jsonschema

        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + CMP_EXT))
        v = jsonschema.Draft4Validator(soi.json_schema)

        for prop in ["none", "expand", "contract"]:
            kwarg = {} if prop == "none" else {prop: True}
            with self.subTest(prop):
                try:
                    v.validate(inv.json_dict(**kwarg))
                except jsonschema.ValidationError:
                    self.fail("'{0}' JSON invalid".format(prop))

    def test_API_Inventory_FlatDictReimport(self):
        """Confirm re-import of a generated flat_dict."""
        from sphobjinv import Inventory, SourceTypes

        inv = Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        inv = Inventory(inv.json_dict())

        self.check_attrs_inventory(inv, SourceTypes.DictJSON, "general")

    def test_API_Inventory_FlatDictReimportWithMetadata(self):
        """Confirm re-import of a generated flat_dict."""
        from sphobjinv import Inventory, SourceTypes

        inv = Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.json_dict()

        d.update({"metadata": "test string"})

        with self.subTest("instantiate_metadata_string"):
            try:
                inv = Inventory(d)
            except Exception:
                self.fail("Failed when instantiating with string metadata")

        self.check_attrs_inventory(
            inv, SourceTypes.DictJSON, "contents_metadata_string"
        )

        d.update({"metadata": {"this": "foo", "that": "bar"}})

        with self.subTest("instantiate_metadata_dict"):
            try:
                inv = Inventory(d)
            except Exception:
                self.fail("Failed when instantiating with dict metadata")

        self.check_attrs_inventory(
            inv, SourceTypes.DictJSON, "contents_metadata_dict"
        )

        d.update({"metadata": 42})

        with self.subTest("instantiate_metadata_int"):
            try:
                inv = Inventory(d)
            except Exception:
                self.fail("Failed when instantiating with int metadata")

        self.check_attrs_inventory(
            inv, SourceTypes.DictJSON, "contents_metadata_int"
        )

    def test_API_Inventory_TooSmallFlatDictImportButIgnore(self):
        """Confirm no error when flat dict passed w/too few objs w/ignore."""
        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.json_dict()
        d.pop("12")

        inv2 = soi.Inventory(d, count_error=False)

        # 55 b/c the loop continues past missing elements
        self.assertEqual(inv2.count, 55)

    def test_API_Inventory_DataFileGenAndReimport(self):
        """Confirm integrated data_file export/import behavior."""
        import os

        import sphobjinv as soi

        for fn in os.listdir(res_path()):
            # Drop unless testall
            if (
                not os.environ.get(TESTALL, False)
                and fn != "objects_attrs.inv"
            ):
                continue

            if fn.startswith("objects_") and fn.endswith(".inv"):
                # Make Inventory
                mch = P_INV.match(fn)
                proj = mch.group(1)
                inv1 = soi.Inventory(res_path(fn))

                # Generate new zlib file and reimport
                data = inv1.data_file()
                cmp_data = soi.compress(data)
                soi.writebytes(scr_path(fn), cmp_data)
                inv2 = soi.Inventory(scr_path(fn))

                # Test the things
                with self.subTest(proj + "_project"):
                    self.assertEqual(inv1.project, inv2.project)
                with self.subTest(proj + "_version"):
                    self.assertEqual(inv1.version, inv2.version)
                with self.subTest(proj + "_count"):
                    self.assertEqual(inv1.count, inv2.count)

                # Only check objects if counts match
                if inv1.count == inv2.count:
                    for i, objs in enumerate(zip(inv1.objects, inv2.objects)):
                        with self.subTest(proj + "_obj" + str(i)):
                            self.assertEqual(objs[0].name, objs[1].name)
                            self.assertEqual(objs[0].domain, objs[1].domain)
                            self.assertEqual(objs[0].role, objs[1].role)
                            self.assertEqual(objs[0].uri, objs[1].uri)
                            self.assertEqual(
                                objs[0].priority, objs[1].priority
                            )
                            self.assertEqual(
                                objs[0].dispname, objs[1].dispname
                            )

    def test_API_Inventory_DataFileGenAndSphinxLoad(self):
        """Confirm Sphinx likes generated inventory files."""
        import os

        import sphobjinv as soi

        for fn in os.listdir(res_path()):
            # Drop unless testall
            if (
                not os.environ.get(TESTALL, False)
                and fn != "objects_attrs.inv"
            ):
                continue

            if fn.startswith("objects_") and fn.endswith(".inv"):
                # Make Inventory
                mch = P_INV.match(fn)
                proj = mch.group(1)
                inv1 = soi.Inventory(res_path(fn))

                # Generate new zlib file
                data = inv1.data_file()
                cmp_data = soi.compress(data)
                soi.writebytes(scr_path(fn), cmp_data)

                # Test the Sphinx load process
                with self.subTest(proj):
                    sphinx_load_test(self, scr_path(fn))

    def test_API_Inventory_NameSuggest(self):
        """Confirm object name suggestion is nominally working."""
        from numbers import Number

        import sphobjinv as soi

        rst = ":py:function:`attr.evolve`"
        idx = 6

        inv = soi.Inventory(res_path(RES_FNAME_BASE + CMP_EXT))

        # No test on the exact fuzzywuzzy match score in these since
        # it could change as fw continues development
        rec = inv.suggest("evolve")

        with self.subTest("plain"):
            self.assertEqual(rec[0], rst)

        rec = inv.suggest("evolve", with_index=True)

        with self.subTest("with_index"):
            self.assertEqual(rec[0][0], rst)
            self.assertEqual(rec[0][1], idx)

        rec = inv.suggest("evolve", with_score=True)

        with self.subTest("with_score"):
            self.assertEqual(rec[0][0], rst)
            self.assertIsInstance(rec[0][1], Number)

        rec = inv.suggest("evolve", with_index=True, with_score=True)

        with self.subTest("with_both"):
            self.assertEqual(rec[0][0], rst)
            self.assertIsInstance(rec[0][1], Number)
            self.assertEqual(rec[0][2], idx)

    def test_API_FuzzyWuzzy_WarningCheck(self):
        """Confirm only the Levenshtein warning is raised, if any are."""
        import warnings

        with warnings.catch_warnings(record=True) as wc:
            warnings.simplefilter("always")
            from fuzzywuzzy import process

            process.__doc__  # Stop flake8 unused import complaint

        # Try to import, and adjust tests accordingly
        try:
            import Levenshtein

            Levenshtein.__doc__  # Stop flake8 complaint
        except ImportError:
            lev_present = False
        else:
            lev_present = True

        if lev_present:
            with self.subTest("count_Lev_present"):  # pragma: no cover
                self.assertEqual(len(wc), 0)

        else:
            with self.subTest("count_Lev_absent"):
                self.assertEqual(len(wc), 1)

            with self.subTest("identity_Lev_absent"):
                # 'message' will be a Warning instance, thus 'args[0]'
                # to retrieve the warning message as str.
                self.assertIn("levenshtein", wc[0].message.args[0].lower())


if __name__ == "__main__":
    print("Module not executable.")
