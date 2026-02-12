r"""*Thread-safety tests for* ``sphobjinv`` *core types*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    7 Feb 2026

**Copyright**
    \(c) Brian Skinn 2016-2025

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

**Members**

"""

from concurrent.futures import ThreadPoolExecutor
from threading import Event, Thread

import pytest

import sphobjinv as soi

pytestmark = [pytest.mark.api, pytest.mark.local]


def _make_obj(name):
    """Create a minimal, valid DataObjStr for tests."""
    return soi.DataObjStr(
        name=name,
        domain="py",
        role="function",
        priority="1",
        uri=f"{name}.html#$",
        dispname="-",
    )


def _inventory_snapshot(inv):
    """Capture a read-only snapshot of an Inventory."""
    return (
        inv.project,
        inv.version,
        inv.count,
        tuple(inv.objects_rst),
        inv.data_file(),
        inv.json_dict(),
        tuple(inv.suggest("evolve", with_index=True, with_score=True)),
    )


def _dataobj_snapshot(obj):
    """Capture a read-only snapshot of a DataObj."""
    return (
        obj.name,
        obj.domain,
        obj.role,
        obj.priority,
        obj.uri,
        obj.dispname,
        obj.uri_contracted,
        obj.uri_expanded,
        obj.dispname_contracted,
        obj.dispname_expanded,
        obj.as_rst,
        obj.data_line(),
        obj.json_dict(),
        obj.as_bytes.json_dict(),
    )


def test_inventory_concurrent_reads_consistent(res_cmp):
    """Concurrent reads of a stable Inventory should be consistent."""
    inv = soi.Inventory(res_cmp)
    expected = _inventory_snapshot(inv)

    def worker():
        for _ in range(25):
            assert _inventory_snapshot(inv) == expected

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(lambda _: worker(), range(8)))


@pytest.mark.parametrize("line_type", (True, False), ids=("expanded", "contracted"))
def test_dataobj_concurrent_reads_consistent(misc_info, line_type):
    """Concurrent reads of a stable DataObj should be consistent."""
    obj = soi.DataObjStr(
        **soi.p_data.search(misc_info.str_lines[line_type]).groupdict()
    )
    expected = _dataobj_snapshot(obj)

    def worker():
        for _ in range(200):
            assert _dataobj_snapshot(obj) == expected

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(lambda _: worker(), range(8)))


def test_inventory_json_dict_not_atomic_during_concurrent_writes():
    """json_dict can observe write interleaving without external locking."""

    class CoordinatedList(list):
        """Coordinate a writer between __len__ and __iter__ calls."""

        def __init__(self, *args):
            super().__init__(*args)
            self.len_called = Event()
            self.allow_iter = Event()

        def __len__(self):
            n = super().__len__()
            self.len_called.set()
            return n

        def __iter__(self):
            # Hold iteration until the test allows it, so we can force a write
            # after count is read but before object rows are emitted.
            assert self.allow_iter.wait(timeout=2)
            return super().__iter__()

    inv = soi.Inventory()
    inv.project = "p"
    inv.version = "v"
    inv.objects = CoordinatedList([_make_obj("first")])

    out = {}

    def reader():
        out["d"] = inv.json_dict()

    t = Thread(target=reader)
    t.start()
    # Ensure json_dict has already consumed len(self.objects), i.e., "count".
    assert inv.objects.len_called.wait(timeout=2)
    # Mutate after count but before object enumeration to force a torn snapshot.
    inv.objects.append(_make_obj("second"))
    # Let json_dict continue into iteration over the now-expanded list.
    inv.objects.allow_iter.set()
    t.join(timeout=2)
    # Reader thread must have completed and produced output for inspection.
    assert "d" in out

    data = out["d"]
    obj_keys = {k for k in data if k.isdigit()}
    # "count" came from pre-mutation len(), so it still reports one object.
    assert data["count"] == 1
    # Enumerated object rows came from post-mutation iteration, yielding two keys.
    assert obj_keys == {"0", "1"}


def test_dataobj_json_dict_not_atomic_during_concurrent_writes():
    """json_dict can observe mixed fields during a multi-attribute update."""
    obj = _make_obj("old")
    name_written = Event()
    finish_write = Event()

    def writer():
        # First half of update: publish new name.
        obj.name = "new"
        name_written.set()
        # Pause before second half so json_dict can read an in-between state.
        assert finish_write.wait(timeout=2)
        # Second half of update: uri catches up afterwards.
        obj.uri = "new.html#$"

    t = Thread(target=writer)
    t.start()
    # Confirm name has been updated before taking the snapshot.
    assert name_written.wait(timeout=2)
    # Read while writer is paused, i.e., during the multi-field transition.
    snapshot = obj.json_dict()
    finish_write.set()
    t.join(timeout=2)

    # Snapshot should include the first write that has already happened.
    assert snapshot["name"] == "new"
    # Snapshot should still include pre-update uri from before second write.
    assert snapshot["uri"] == "old.html#$"
