r"""*Direct, NONLOCAL expect-good API tests for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    21 Mar 2019

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


pytestmark = [pytest.mark.api, pytest.mark.good]


@pytest.mark.skip("Un-converted tests")
class TestSphobjinvAPIInvGoodNonlocal(SuperSphobjinv, ut.TestCase):
    """Testing Inventory URL download import method.

    The test in this class is SLOW. For routine testing work, invoke tests.py
    with '--local', rather than '--all', to avoid running it.

    """

    def test_API_Inventory_ManyURLImports(self):
        """Confirm a plethora of .inv files downloads properly via url arg."""
        import os

        from sphobjinv import Inventory as Inv

        for fn in os.listdir(res_path()):
            # Drop unless testall
            if not os.environ.get(TESTALL, False) and fn != "objects_attrs.inv":
                continue

            mch = P_INV.match(fn)
            if mch is not None:
                name = mch.group(1)
                inv1 = Inv(res_path(fn))
                inv2 = Inv(url=REMOTE_URL.format(name))
                with self.subTest(name + "_project"):
                    self.assertEqual(inv1.project, inv2.project)
                with self.subTest(name + "_version"):
                    self.assertEqual(inv1.version, inv2.version)
                with self.subTest(name + "_count"):
                    self.assertEqual(inv1.count, inv2.count)

                # Only check objects if counts match
                if inv1.count == inv2.count:
                    for i, objs in enumerate(zip(inv1.objects, inv2.objects)):
                        with self.subTest(name + "_obj" + str(i)):
                            self.assertEqual(objs[0].name, objs[1].name)
                            self.assertEqual(objs[0].domain, objs[1].domain)
                            self.assertEqual(objs[0].role, objs[1].role)
                            self.assertEqual(objs[0].uri, objs[1].uri)
                            self.assertEqual(objs[0].priority, objs[1].priority)
                            self.assertEqual(objs[0].dispname, objs[1].dispname)


if __name__ == "__main__":
    print("Module not executable.")
