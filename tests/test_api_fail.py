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


pytestmark = [pytest.mark.api, pytest.mark.fail]


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
    from zlib import error as ZlibError

    # OS-dependent. VersionError on Windows b/c bytes import of the
    # text-file objects_attrs.txt has the first line ending with b'2\r\n',
    # whereas *nix will pass the version check but choke in the zlib
    # decompression process
    with pytest.raises((ZlibError, soi.VersionError)):
        soi.Inventory(fname_zlib=res_dec)


@pytest.mark.parametrize("dobj", [soi.DataObjBytes, soi.DataObjStr])
def test_apifail_bad_dataobj_init_types(dobj):
    """Confirm error raised when init-ed w/wrong types."""
    with pytest.raises(TypeError):
        dobj(*range(6))


@pytest.mark.xfail(reason="Changed to mutable to avoid Inventory revision pain")
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


@pytest.mark.skip("Un-converted tests")
class TestSphobjinvAPIExpectFail(SuperSphobjinv, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    def test_API_DataLine_BothArgsTrue(self):
        """Confirm error raised when both expand and contract are True."""
        import sphobjinv as soi

        dos = soi.DataObjStr(**soi.p_data.search(S_LINES_0[True]).groupdict())
        with self.assertRaises(ValueError):
            dos.data_line(expand=True, contract=True)

    def test_API_Inventory_InvalidSource(self):
        """Confirm error raised when invalid source provided."""
        import sphobjinv as soi

        with self.assertRaises(TypeError):
            soi.Inventory("abcdefg")

    def test_API_Inventory_NoItemsFlatDict(self):
        """Confirm TypeError with no-items dict passed to json_dict."""
        import sphobjinv as soi

        d = {
            soi.HeaderFields.Project.value: "proj",
            soi.HeaderFields.Version.value: "v3.3",
            soi.HeaderFields.Count.value: 5,
        }

        self.assertRaises(TypeError, soi.Inventory._import_json_dict, d)

    def test_API_Inventory_TooSmallDictImport(self):
        """Confirm error raised when JSON dict passed w/too few objects."""
        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.json_dict()
        d.pop("12")

        self.assertRaises(ValueError, soi.Inventory, d)

    def test_API_Inventory_BadObjDictImport(self):
        """Confirm error raised when JSON dict passed w/an invalid object."""
        from jsonschema.exceptions import ValidationError
        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.json_dict()
        d.update({"112": "foobarbazquux"})

        self.assertRaises(ValidationError, soi.Inventory, dict_json=d)

    def test_API_Inventory_TooBigJSONDictImport(self):
        """Confirm error raised when JSON dict passed w/too many objects."""
        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.json_dict()
        d.update({"57": d["23"]})

        self.assertRaises(ValueError, soi.Inventory, dict_json=d)

    def test_API_Inventory_BadRootObjectJSONDictImport(self):
        """Confirm error raised when spurious extra root object present."""
        import sphobjinv as soi
        from jsonschema.exceptions import ValidationError

        inv = soi.Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.json_dict()
        d.update({"bad_foo": "angry_bar"})

        self.assertRaises(ValidationError, soi.Inventory, dict_json=d)

    def test_API_Inventory_TooManyInitSrcArgs(self):
        """Confirm error if >1 sources passed."""
        from sphobjinv import Inventory

        self.assertRaises(RuntimeError, Inventory, source="foo", plaintext="bar")

    def test_API_Inventory_NoObjectInventories(self):
        """Confirm no-objects inventories don't import."""
        import sphobjinv as soi

        inv = soi.Inventory()

        with self.subTest("plain"):
            self.assertRaises(TypeError, soi.Inventory, inv.data_file())

        with self.subTest("zlib"):
            # Actually testing that importing an empty inventory
            # blows up, not importing one
            self.assertRaises(
                (TypeError, ValueError), soi.Inventory, soi.compress(inv.data_file())
            )

        d = {"project": "test", "version": "0.0", "count": 0}
        with self.subTest("json"):
            self.assertRaises(ValueError, soi.Inventory, d)


if __name__ == "__main__":
    print("Module not executable.")
