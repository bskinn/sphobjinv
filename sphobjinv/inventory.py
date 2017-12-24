"""
Module defining the Inventory object for holding entire Sphinx inventories.

Name:        inventory.py
Exposes:     SourceTypes (Enum) -- Types of source objects intelligible
                                   to an Inventory
             Inventory (class)  -- Object providing methods for parsing,
                                   manipulating, and exporting Sphinx
                                   objects.inv inventories.

Author:      Brian Skinn (bskinn@alum.mit.edu)

Created:     7 Dec 2017
Copyright:   (c) Brian Skinn 2016-2017
License:     The MIT License; see "LICENSE.txt" for full license terms
             and contributor agreement.

This file is part of Sphinx Objects.inv Encoder/Decoder, a toolkit for
encoding and decoding objects.inv files for use with intersphinx.

http://www.github.com/bskinn/sphobjinv

"""

from enum import Enum

import attr

from .data import DataObjStr, HeaderFields


class SourceTypes(Enum):
    """Enum for the import mode used in instantiating an Inventory.

    Since Enum keys remain ordered in definition sequence, the
    definition order here defines the order in which Inventory
    objects attempt to parse source objects passed to __init__().

    """

    Manual = 'manual'
    BytesPlaintext = 'bytes_plain'
    BytesZlib = 'bytes_zlib'
    FnamePlaintext = 'fname_plain'
    FnameZlib = 'fname_zlib'
    DictFlat = 'dict_flat'
    DictStruct = 'dict_struct'


@attr.s(slots=True, cmp=False)
class Inventory(object):
    """Entire contents of an objects.inv inventory.

    All information stored within as str, even if imported
    from a bytes source.

    """

    from copy import deepcopy as _deepcopy

    _source = attr.ib(repr=False, convert=_deepcopy, default=None)
    project = attr.ib(init=False, default=None)
    version = attr.ib(init=False, default=None)
    objects = attr.ib(init=False, default=attr.Factory(list))
    source_type = attr.ib(init=False, default=None)

    @property
    def count(self):
        """Return the number of objects currently in inventory."""
        return len(self.objects)

    @property
    def flat_dict(self):
        """Generate a flat dict representation of the inventory as-is."""
        d = {HeaderFields.Project.value: self.project,
             HeaderFields.Version.value: self.version,
             HeaderFields.Count.value: self.count}

        for i, o in enumerate(self.objects):
            d.update({str(i): o.flat_dict()})

        return d

    @property
    def flat_dict_expanded(self):
        """Generate an expanded flat dict representation."""
        d = {HeaderFields.Project.value: self.project,
             HeaderFields.Version.value: self.version,
             HeaderFields.Count.value: self.count}

        for i, o in enumerate(self.objects):
            d.update({str(i): o.flat_dict(expand=True)})

        return d

    @property
    def flat_dict_contracted(self):
        """Generate a contracted flat dict representation."""
        d = {HeaderFields.Project.value: self.project,
             HeaderFields.Version.value: self.version,
             HeaderFields.Count.value: self.count}

        for i, o in enumerate(self.objects):
            d.update({str(i): o.flat_dict(contract=True)})

        return d

    @property
    def struct_dict(self):
        """Generate a structured dict representation."""
        d = {HeaderFields.Project.value: self.project,
             HeaderFields.Version.value: self.version,
             HeaderFields.Count.value: self.count}

        for o in self.objects:
            o.update_struct_dict(d)

        return d

    @property
    def struct_dict_expanded(self):
        """Generate an expanded structured dict representation."""
        d = {HeaderFields.Project.value: self.project,
             HeaderFields.Version.value: self.version,
             HeaderFields.Count.value: self.count}

        for o in self.objects:
            o.update_struct_dict(d, expand=True)

        return d

    @property
    def struct_dict_contracted(self):
        """Generate a contracted structured dict representation."""
        d = {HeaderFields.Project.value: self.project,
             HeaderFields.Version.value: self.version,
             HeaderFields.Count.value: self.count}

        for o in self.objects:
            o.update_struct_dict(d, contract=True)

        return d

    @property
    def objects_rst(self):
        """Generate a list of the objects in a reST-like representation."""
        return list(_.as_rst for _ in self.objects)

    def __str__(self):  # pragma: no cover
        """Return concise, readable description of contents."""
        ret_str = "<{0} ({1}): {2} v{3}, {4} objects>"

        return ret_str.format(type(self).__name__, self.source_type.value,
                              self.project, self.version, self.count)

    def __attrs_post_init__(self):
        """Construct the inventory from the indicated source."""
        from zlib import error as ZlibError

        # Lookups for method names and expected import-failure errors
        importers = {SourceTypes.BytesPlaintext: self._import_plaintext_bytes,
                     SourceTypes.BytesZlib: self._import_zlib_bytes,
                     SourceTypes.FnamePlaintext: self._import_plaintext_fname,
                     SourceTypes.FnameZlib: self._import_zlib_fname,
                     SourceTypes.DictFlat: self._import_flat_dict,
                     SourceTypes.DictStruct: self._import_struct_dict,
                     }
        import_errors = {SourceTypes.BytesPlaintext: TypeError,
                         SourceTypes.BytesZlib: (ZlibError, TypeError),
                         SourceTypes.FnamePlaintext: (FileNotFoundError,
                                                      TypeError),
                         SourceTypes.FnameZlib: (FileNotFoundError,
                                                 TypeError,
                                                 ZlibError),
                         SourceTypes.DictFlat: TypeError,
                         SourceTypes.DictStruct: TypeError,
                         }

        # Leave uninitialized ("manual" init) if _source is None
        if self._source is None:
            self.source_type = SourceTypes.Manual
            return

        # Attempt series of import approaches
        for st in SourceTypes:  # Enum keys are ordered, so iteration is too.
            if st == SourceTypes.Manual:
                continue

            if self._try_import(importers[st], import_errors[st]):
                self.source_type = st
                return

        # Nothing worked, complain.
        raise TypeError('Invalid Inventory source type')

    def _try_import(self, import_fxn, exc):
        """Attempt the indicated import method.

        Returns True on success.

        """
        try:
            p, v, o = import_fxn(self._source)
        except exc:
            return False

        self.project = p
        self.version = v
        self.objects = o

        return True

    def _import_plaintext_bytes(self, b_str):
        """Import an inventory from plaintext bytes."""
        from .re import pb_data, pb_project, pb_version

        b_res = pb_project.search(b_str).group(HeaderFields.Project.value)
        project = b_res.decode('utf-8')

        b_res = pb_version.search(b_str).group(HeaderFields.Version.value)
        version = b_res.decode('utf-8')

        def gen_dataobjs():
            for mch in pb_data.finditer(b_str):
                yield DataObjStr(**mch.groupdict())

        objects = []
        list(map(objects.append, gen_dataobjs()))

        if len(objects) == 0:
            raise TypeError  # Wrong bytes file contents

        return project, version, objects

    def _import_zlib_bytes(self, b_str):
        """Import a zlib-compressed inventory."""
        from .zlib import decode

        b_plain = decode(b_str)
        p, v, o = self._import_plaintext_bytes(b_plain)

        return p, v, o

    def _import_plaintext_fname(self, fn):
        """Import a plaintext inventory file."""
        from .fileops import readfile

        b_plain = readfile(fn)

        return self._import_plaintext_bytes(b_plain)

    def _import_zlib_fname(self, fn):
        """Import a zlib-compressed inventory file."""
        from .fileops import readfile

        b_zlib = readfile(fn)

        return self._import_zlib_bytes(b_zlib)

    def _import_flat_dict(self, d):
        """Import flat-dict composited data."""
        from copy import copy

        from .data import DataObjStr

        # Attempting to pull these first, so that if it's not a dict,
        # the TypeError will get raised before the below shallow-copy.
        project = d[HeaderFields.Project.value]
        version = d[HeaderFields.Version.value]
        count = d[HeaderFields.Count.value]

        # If not even '1' is in the dict, assume invalid type due to
        # it being a struct_dict format.
        if '1' not in d:
            raise TypeError('No str(int)-indexed data object items found.')

        # Going to destructively process d, so shallow-copy it first
        d = copy(d)

        # Expecting the dict to be indexed by string integers
        objects = []
        for i in range(count):
            try:
                objects.append(DataObjStr(**d.pop(str(i))))
            except KeyError as e:
                err_str = ("Too few objects found in dict "
                           "(halt at {0}, expect {1})".format(i, count))
                raise ValueError(err_str) from e

        # Complain if len of remaining dict is other than 3
        if len(d) != 3:  # project, version, count
            err_str = ("Too many objects in dict "
                       "({0}, expect {1})".format(count + len(d) - 3, count))
            raise ValueError(err_str)

        # Should be good to return
        return project, version, objects

    def _import_struct_dict(self, d):
        """Import struct-dict composited data."""
        from .data import DataObjStr

        # Attempting to pull these first, so that if it's not a dict,
        # the TypeError will get raised before the below extensive
        # parsing.
        project = d[HeaderFields.Project.value]
        version = d[HeaderFields.Version.value]
        count = d[HeaderFields.Count.value]

        # Init 'objects' for later filling
        objects = []

        # Loop over everything that's not a known struct-dict
        # header field. These will be domains.
        for domain in d:
            if domain in (HeaderFields.Project.value,
                          HeaderFields.Version.value,
                          HeaderFields.Count.value,
                          HeaderFields.Metadata.value):
                continue

            domain_dict = d[domain]

            # Next level in will be roles
            for role in domain_dict:
                role_dict = domain_dict[role]

                # Final level is names
                for name in role_dict:
                    name_dict = role_dict[name]

                    # Create DataObj and add to .objects
                    objects.append(DataObjStr(domain=domain, role=role,
                                              name=name, **name_dict))

        # Confirm count
        if count != len(objects):
            raise ValueError('{0} objects found '.format(len(objects)) +
                             '(expect {0})'.format(count))

        # Return info
        return project, version, objects

    def suggest(self, name, *, thresh=75):
        """Suggest objects in the inventory to match a name."""
        import warnings

        # Suppress any UserWarning about the speed issue
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            from fuzzywuzzy import process as fwp

        return list(_ for _ in fwp.extract(name, self.objects_rst,
                                           limit=None) if _[1] > thresh)
