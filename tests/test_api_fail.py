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


@pytest.mark.skip("Un-converted tests")
class TestSphobjinvAPIExpectFail(SuperSphobjinv, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    def test_API_NoInputFile(self):
        """Confirm that appropriate exceptions are raised w/no input file."""
        import sphobjinv as soi

        with self.subTest("decomp_input_file"):
            with self.assertRaises(FileNotFoundError):
                soi.readbytes(INIT_FNAME_BASE + DEC_EXT)

        with self.subTest("comp_input_file"):
            with self.assertRaises(FileNotFoundError):
                soi.readbytes(INIT_FNAME_BASE + CMP_EXT)

    def test_API_WriteFileBadOutputFile(self):
        """Confirm OSError raised on bad filename (example of read error)."""
        import sphobjinv as soi

        b_str = b"This is a binary string!"

        with self.assertRaises(OSError):
            soi.writebytes(INVALID_FNAME, b_str)

    def test_API_ErrorDecompressingPlaintext(self):
        """Confirm error raised on attempt to decompress plaintext."""
        from zlib import error as ZlibError

        import sphobjinv as soi

        # OS-dependent. VersionError on Windows b/c bytes import of the
        # text-file objects_attrs.txt has the first line ending with b'2\r\n',
        # whereas *nix will pass the version check but choke in the zlib
        # decompression process
        self.assertRaises(
            (ZlibError, soi.VersionError),
            soi.Inventory,
            fname_zlib=res_path(RES_FNAME_BASE + DEC_EXT),
        )

    def test_API_BadDataObjInitTypes(self):
        """Confirm error raised when init-ed w/wrong types."""
        import sphobjinv as soi

        with self.subTest("bytes"):
            with self.assertRaises(TypeError):
                soi.DataObjBytes(*range(6))

        with self.subTest("str"):
            with self.assertRaises(TypeError):
                soi.DataObjStr(*range(6))

    @ut.skip("Changed to mutable to avoid Inventory revision pain.")
    def test_API_ChangingImmutableDataObj(self):
        """Confirm DataObj's are immutable."""
        from attr.exceptions import FrozenInstanceError as FIError

        from sphobjinv import Inventory as Inv

        inv = Inv(res_path(RES_FNAME_BASE + CMP_EXT))

        with self.subTest("str"):
            with self.assertRaises(FIError):
                inv.objects[0].name = "newname"
        with self.subTest("bytes"):
            with self.assertRaises(FIError):
                inv.objects[0].as_bytes.name = b"newname"

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

        self.assertRaises(
            RuntimeError, Inventory, source="foo", plaintext="bar"
        )

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
                (TypeError, ValueError),
                soi.Inventory,
                soi.compress(inv.data_file()),
            )

        d = {"project": "test", "version": "0.0", "count": 0}
        with self.subTest("json"):
            self.assertRaises(ValueError, soi.Inventory, d)


if __name__ == "__main__":
    print("Module not executable.")
