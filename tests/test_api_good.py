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

import itertools as itt
import re
from pathlib import Path

import pytest

import sphobjinv as soi


pytestmark = [pytest.mark.api, pytest.mark.local]


with (Path(__file__).resolve().parent / "testall_inv_paths.py").open() as f:
    exec(f.read())


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
        misc_info.FNames.INIT_FNAME_BASE.value + misc_info.Extensions.DEC_EXT.value
    )
    dest_path = scratch_path / (
        misc_info.FNames.MOD_FNAME_BASE.value + misc_info.Extensions.CMP_EXT.value
    )

    try:
        b_dec = soi.readbytes(str(src_path))
        b_cmp = soi.compress(b_dec)
        soi.writebytes(str(dest_path), b_cmp)
    except Exception:
        pytest.fail("objects.txt compression failed.")

    assert dest_path.is_file()

    sphinx_load_test(dest_path)


def test_api_decompress(scratch_path, misc_info, decomp_cmp_test):
    """Check that a decompress attempt via API throws no errors."""
    src_path = scratch_path / (
        misc_info.FNames.INIT_FNAME_BASE.value + misc_info.Extensions.CMP_EXT.value
    )
    dest_path = scratch_path / (
        misc_info.FNames.MOD_FNAME_BASE.value + misc_info.Extensions.DEC_EXT.value
    )

    try:
        b_cmp = soi.readbytes(str(src_path))
        b_dec = soi.decompress(b_cmp)
        soi.writebytes(str(dest_path), b_dec)
    except Exception:
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

    assert mchs[element].groupdict() == {_.value: datadict[_] for _ in datadict}


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

    assert b_dos == s_dos

    assert all(
        [
            getattr(s_dos, _) == getattr(b_dos.as_bytes, _).decode("utf-8")
            for _ in s_mchdict
        ]
    )


def test_api_dataobjbytes_flatdictfxn(bytes_txt):
    """Confirm that flat dict generating function works."""
    mch = soi.pb_data.search(bytes_txt)

    b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
    b_jsondict = soi.DataObjBytes(**b_mchdict).json_dict()

    assert b_mchdict == b_jsondict


def test_api_dataobjstr_flatdictfxn(bytes_txt):
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
    ids=(lambda i: i if type(i) == str else ""),
)
@pytest.mark.parametrize("dataline_arg", (True, False))
@pytest.mark.parametrize("init_expanded", (True, False))
def test_api_dataobj_datalinefxn(
    dataobjtype, regex, lines, init_expanded, dataline_arg, misc_info, subtests
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
    with subtests.test(msg="expand"):
        dl = dobj.data_line(expand=dataline_arg)
        assert dl == lines_obj[dataline_arg or init_expanded]

    # If dataline_arg is False, should match the value of init_expanded.
    # If dataline_arg is True, should match the False (contracted) value.
    # Thus, the only True (expanded) situation is when init_expanded == True
    # and and dataline_arg == False.
    with subtests.test(msg="contract"):
        dl = dobj.data_line(contract=dataline_arg)
        assert dl == lines_obj[init_expanded and not dataline_arg]


@pytest.mark.xfail(
    reason="Will fail until .as_xxx properties are removed from attrs cmp"
)
@pytest.mark.parametrize(
    "use_bytes", (True, False), ids=(lambda b: "use_bytes_" + str(b))
)
def test_api_dataobj_evolvename(use_bytes, res_cmp):
    """Confirm evolving new DataObj instances works properly."""
    inv = soi.Inventory(res_cmp)
    obj = inv.objects[5].as_bytes if use_bytes else inv.objects[5]  # Arbitrary choice
    oldname = obj.name

    newname = b"foo" if use_bytes else "foo"
    obj2 = obj.evolve(name=newname)
    obj3 = obj2.evolve(name=oldname)

    assert obj == obj3
    assert obj2.name == newname


def test_api_inventory_default_none_instantiation(subtests):
    """Confirm 'manual' instantiation with None."""
    inv = soi.Inventory()

    with subtests.test(msg="project"):
        assert inv.project is None

    with subtests.test(msg="version"):
        assert inv.version is None

    with subtests.test(msg="count"):
        assert inv.count == 0

    with subtests.test(msg="source_type"):
        assert inv.source_type is soi.SourceTypes.Manual


@pytest.mark.parametrize(
    ["source_type", "inv_arg"],
    [
        (soi.SourceTypes.BytesPlaintext, "plaintext"),
        (soi.SourceTypes.BytesZlib, "zlib"),
        (soi.SourceTypes.FnamePlaintext, "fname_plain"),
        (soi.SourceTypes.FnameZlib, "fname_zlib"),
    ],
    ids=(lambda v: v if type(v) == str else ""),
)
def test_api_inventory_bytes_fname_instantiation(
    source_type, inv_arg, res_path, misc_info, attrs_inventory_test, subtests
):
    """Check bytes and filename modes for Inventory instantiation."""
    source = str(res_path / misc_info.FNames.RES_FNAME_BASE.value)

    if source_type in (soi.SourceTypes.BytesPlaintext, soi.SourceTypes.FnamePlaintext):
        source += misc_info.Extensions.DEC_EXT.value
    else:
        source += misc_info.Extensions.CMP_EXT.value

    if source_type in (soi.SourceTypes.BytesPlaintext, soi.SourceTypes.BytesZlib):
        source = soi.readbytes(source)

    # General import, without a specified kwarg
    with subtests.test(msg="general"):
        attrs_inventory_test(soi.Inventory(source), source_type)

    # Importing with the respective kwarg for each source type
    with subtests.test(msg="specific"):
        inv = soi.Inventory(**{inv_arg: source})
        attrs_inventory_test(inv, source_type)

    # Special case for plaintext bytes, try decoding it
    if source_type is soi.SourceTypes.BytesPlaintext:
        with subtests.test(msg="plaintext_bytes"):
            inv = soi.Inventory(**{inv_arg: source.decode("utf-8")})
            attrs_inventory_test(inv, source_type)


@pytest.mark.parametrize("prop", ("none", "expand", "contract"))
def test_api_inventory_flatdict_jsonvalidate(prop, res_cmp):
    """Confirm that the flat_dict properties generated valid JSON."""
    import jsonschema

    inv = soi.Inventory(res_cmp)
    val = jsonschema.Draft4Validator(soi.json_schema)

    kwarg = {} if prop == "none" else {prop: True}
    try:
        val.validate(inv.json_dict(**kwarg))
    except jsonschema.ValidationError:
        pytest.fail("'{}' JSON invalid".format(prop))


def test_api_inventory_flatdict_reimport(res_dec, attrs_inventory_test):
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
    metadata, res_dec, attrs_inventory_test
):
    """Confirm re-import of a generated flat_dict with metadata."""
    inv = soi.Inventory(res_dec)
    d = inv.json_dict()

    d.update({"metadata": metadata})
    try:
        inv = soi.Inventory(d)
    except Exception:
        pytest.fail("Instantiation fail on metadata '{}'".format(metadata))

    attrs_inventory_test(inv, soi.SourceTypes.DictJSON)


def test_api_inventory_toosmallflatdict_importbutignore(res_dec):
    """Confirm no error when flat dict passed w/too few objs w/ignore."""
    inv = soi.Inventory(res_dec)
    d = inv.json_dict()
    d.pop("12")

    inv2 = soi.Inventory(d, count_error=False)

    # 55 b/c the loop continues past missing elements
    assert inv2.count == 55


def test_api_inventory_namesuggest(res_cmp, subtests):
    """Confirm object name suggestion is nominally working."""
    from numbers import Number

    rst = ":py:function:`attr.evolve`"
    idx = 6

    inv = soi.Inventory(str(res_cmp))

    # No test on the exact fuzzywuzzy match score in these since
    # it could change as fw continues development
    with subtests.test(msg="basic"):
        assert inv.suggest("evolve")[0] == rst

    with subtests.test(msg="index"):
        assert inv.suggest("evolve", with_index=True)[0] == (rst, idx)

    with subtests.test(msg="score"):
        rec = inv.suggest("evolve", with_score=True)
        assert rec[0][0] == rst
        assert isinstance(rec[0][1], Number)

    with subtests.test(msg="index_and_score"):
        rec = inv.suggest("evolve", with_index=True, with_score=True)
        assert rec[0][0] == rst
        assert isinstance(rec[0][1], Number)
        assert rec[0][2] == idx


# Must be run first, otherwise the fuzzywuzzy warning is consumed
# inappropriately
@pytest.mark.first
def test_api_fuzzywuzzy_warningcheck():
    """Confirm only the Levenshtein warning is raised, if any are."""
    import warnings

    with warnings.catch_warnings(record=True) as wc:
        warnings.simplefilter("always")
        from fuzzywuzzy import process  # noqa: F401

    # Try to import, and adjust tests accordingly
    try:
        import Levenshtein  # noqa: F401
    except ImportError:
        lev_present = False
    else:
        lev_present = True

    if lev_present:
        assert len(wc) == 0, "Warning unexpectedly raised"  # pragma: no cover
    else:
        assert len(wc) == 1, "Warning unexpectedly not raised"

        # 'message' will be a Warning instance, thus 'args[0]'
        # to retrieve the warning message as str.
        assert (
            "levenshtein" in wc[0].message.args[0].lower()
        ), "Warning raised for unexpected reason"


@pytest.mark.parametrize("inv_path", list(testall_inv_paths), ids=(lambda p: p.name))
@pytest.mark.testall
def test_api_inventory_datafile_gen_and_reimport(
    inv_path,
    res_path,
    scratch_path,
    misc_info,
    sphinx_load_test,
    pytestconfig,
    subtests,
):
    """Confirm integrated data_file export/import behavior."""
    fname = inv_path.name
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
    with subtests.test(msg="content"):
        assert inv1.project == inv2.project
        assert inv1.version == inv2.version
        assert inv1.count == inv2.count
        for objs in zip(inv1.objects, inv2.objects):
            assert objs[0].name == objs[1].name
            assert objs[0].domain == objs[1].domain
            assert objs[0].role == objs[1].role
            assert objs[0].uri == objs[1].uri
            assert objs[0].priority == objs[1].priority
            assert objs[0].dispname == objs[1].dispname

    # Ensure sphinx likes the regenerated inventory
    with subtests.test(msg="sphinx_load"):
        sphinx_load_test(scr_fpath)


if __name__ == "__main__":
    print("Module not executable.")
