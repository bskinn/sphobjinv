r"""*Direct expect-fail API tests for* ``sphobjinv``.

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

import pytest

import sphobjinv as soi


pytestmark = [pytest.mark.api, pytest.mark.local]


def test_apifail_readbytes_missing_input_file(scratch_path):
    """Confirm that appropriate exception is raised w/no input file."""
    with pytest.raises(FileNotFoundError):
        soi.readbytes(str(scratch_path / "thisfilewillneverexist.foo"))


def test_apifail_writebytes_badoutputfile(scratch_path, misc_info):
    """Confirm OSError raised on bad filename (example of read error)."""
    b_str = b"This is a binary string!"

    with pytest.raises(OSError):
        soi.writebytes(misc_info.invalid_filename, b_str)


def test_apifail_error_decompressing_plaintext(res_dec):
    """Confirm error raised on attempt to decompress plaintext."""
    from zlib import error as zlib_error

    # OS-dependent. VersionError on Windows b/c bytes import of the
    # text-file objects_attrs.txt has the first line ending with b'2\r\n',
    # whereas *nix will pass the version check but choke in the zlib
    # decompression process
    with pytest.raises((zlib_error, soi.VersionError)):
        soi.Inventory(fname_zlib=res_dec)


@pytest.mark.parametrize("dobj", [soi.DataObjBytes, soi.DataObjStr])
def test_apifail_bad_dataobj_init_types(dobj):
    """Confirm error raised when init-ed w/wrong types."""
    with pytest.raises(TypeError):
        dobj(*range(6))


@pytest.mark.xfail(reason="Made mutable to simplify Inventory revision by users")
@pytest.mark.parametrize("use_bytes", [True, False])
def test_apifail_changing_immutable_dataobj(use_bytes, res_cmp):
    """Confirm DataObj's are immutable."""
    from attr.exceptions import FrozenInstanceError as FIError

    inv = soi.Inventory(res_cmp)

    with pytest.raises(FIError):
        if use_bytes:
            inv.objects[0].as_bytes.name = b"newname"
        else:
            inv.objects[0].name = "newname"


def test_apifail_dataline_bothargstrue(misc_info):
    """Confirm error raised when both expand and contract are True."""
    dos = soi.DataObjStr(**soi.p_data.search(misc_info.str_lines[True]).groupdict())
    with pytest.raises(ValueError):
        dos.data_line(expand=True, contract=True)


def test_apifail_inventory_invalidsource():
    """Confirm error raised when invalid source provided."""
    with pytest.raises(TypeError):
        soi.Inventory("abcdefg")


def test_apifail_inventory_dictimport_noitems():
    """Confirm ValueError with no-items dict passed to json_dict."""
    d = {
        soi.HeaderFields.Project.value: "proj",
        soi.HeaderFields.Version.value: "v3.3",
        soi.HeaderFields.Count.value: 5,
    }

    with pytest.raises(ValueError):
        soi.Inventory()._import_json_dict(d)


def test_apifail_inventory_dictimport_toosmall(res_dec):
    """Confirm error raised when JSON dict passed w/too few objects."""
    inv = soi.Inventory(res_dec)
    d = inv.json_dict()
    d.pop("12")

    with pytest.raises(ValueError):
        soi.Inventory(d)


def test_apifail_inventory_dictimport_badobj(res_dec):
    """Confirm error raised when JSON dict passed w/an invalid object."""
    from jsonschema.exceptions import ValidationError

    inv = soi.Inventory(res_dec)
    d = inv.json_dict()
    d.update({"112": "foobarbazquux"})

    with pytest.raises(ValidationError):
        soi.Inventory(dict_json=d)


def test_apifail_inventory_dictimport_toobig(res_dec):
    """Confirm error raised when JSON dict passed w/too many objects."""
    inv = soi.Inventory(res_dec)
    d = inv.json_dict()
    d.update({"57": d["23"]})

    with pytest.raises(ValueError):
        soi.Inventory(dict_json=d)


def test_apifail_inventory_dictimport_badrootobject(res_dec):
    """Confirm error raised when spurious extra root object present."""
    from jsonschema.exceptions import ValidationError

    inv = soi.Inventory(res_dec)
    d = inv.json_dict()
    d.update({"bad_foo": "angry_bar"})

    with pytest.raises(ValidationError):
        soi.Inventory(dict_json=d)


def test_apifail_inventory_dictimport_toomanysrcargs():
    """Confirm error if >1 sources passed."""
    with pytest.raises(RuntimeError):
        soi.Inventory(source="foo", plaintext="bar")


def test_apifail_inventory_no_object_invs(subtests):
    """Confirm no-objects inventories don't import."""
    inv = soi.Inventory()

    with subtests.test(msg="plain"):
        with pytest.raises(TypeError):
            soi.Inventory(inv.data_file())

    with subtests.test(msg="zlib"):
        with pytest.raises((TypeError, ValueError)):
            soi.Inventory(soi.compress(inv.data_file()))

    d = {"project": "test", "version": "0.0", "count": 0}
    with subtests.test(msg="json"):
        with pytest.raises(ValueError):
            soi.Inventory(d)


if __name__ == "__main__":
    print("Module not executable.")
