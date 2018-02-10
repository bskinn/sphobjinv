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
Copyright:   (c) Brian Skinn 2016-2018
License:     The MIT License; see "LICENSE.txt" for full license terms
             and contributor agreement.

This file is part of Sphinx Objects.inv Encoder/Decoder, a toolkit for
encoding and decoding objects.inv files for use with intersphinx.

http://www.github.com/bskinn/sphobjinv

"""

from enum import Enum

import attr

from .data import DataObjStr


class HeaderFields(Enum):
    """Enum for regex groups of objects.inv header data."""

    Project = 'project'
    Version = 'version'
    Count = 'count'
    Objects = 'objects'
    Metadata = 'metadata'


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
    DictJSON = 'dict_json'
    URL = 'url'


@attr.s(slots=True, cmp=False)
class Inventory(object):
    """Entire contents of an objects.inv inventory.

    All information stored within as str, even if imported
    from a bytes source.

    """

    # General source for try-most-types import
    # Needs to be first so it absorbs a positional arg
    _source = attr.ib(repr=False, default=None)

    # Stringlike types (both accept str & bytes)
    _plaintext = attr.ib(repr=False, default=None)
    _zlib = attr.ib(repr=False, default=None)

    # Filename types (must be str)
    _fname_plain = attr.ib(repr=False, default=None)
    _fname_zlib = attr.ib(repr=False, default=None)

    # dict types
    _dict_json = attr.ib(repr=False, default=None)

    # URL for remote retrieval of objects.inv/.txt
    _url = attr.ib(repr=False, default=None)

    # Flag for whether to raise error on object count mismatch
    _count_error = attr.ib(repr=False, default=True,
                           validator=attr.validators.instance_of(bool))

    # Actual regular attributes
    project = attr.ib(init=False, default=None)
    version = attr.ib(init=False, default=None)
    objects = attr.ib(init=False, default=attr.Factory(list))
    source_type = attr.ib(init=False, default=None)

    # Helper strings for inventory datafile output
    header_preamble = '# Sphinx inventory version 2'
    header_project = '# Project: {project}'
    header_version = '# Version: {version}'
    header_zlib = '# The remainder of this file is compressed using zlib.'

    @property
    def count(self):
        """Return the number of objects currently in inventory."""
        return len(self.objects)

    def json_dict(self, expand=False, contract=False):
        """Generate a flat dict representation of the inventory."""
        d = {HeaderFields.Project.value: self.project,
             HeaderFields.Version.value: self.version,
             HeaderFields.Count.value: self.count}

        for i, o in enumerate(self.objects):
            d.update({str(i): o.json_dict(expand=expand,
                                          contract=contract)})

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
        from .data import _utf8_encode

        # List of sources
        src_list = (self._source, self._plaintext, self._zlib,
                    self._fname_plain, self._fname_zlib,
                    self._dict_json, self._url)
        src_count = sum(1 for _ in src_list if _ is not None)

        # Complain if multiple sources provided
        if src_count > 1:
            raise RuntimeError('At most one data source can '
                               'be specified.')

        # Leave uninitialized ("manual" init) if no source provided
        if src_count == 0:
            self.source_type = SourceTypes.Manual
            return

        # If general ._source was provided, run the generalized import
        if self._source is not None:
            self._general_import()
            return

        # For all of these below, '()' is passed as 'exc' argument since
        # desire _try_import not to handle any exception types

        # Plaintext str or bytes
        # Special case, since preconverting input.
        if self._plaintext is not None:
            self._try_import(self._import_plaintext_bytes,
                             _utf8_encode(self._plaintext),
                             ())
            self.source_type = SourceTypes.BytesPlaintext
            return

        # Remainder are iterable
        for src, fxn, st in zip((self._zlib, self._fname_plain,
                                 self._fname_zlib, self._dict_json,
                                 self._url),
                                (self._import_zlib_bytes,
                                 self._import_plaintext_fname,
                                 self._import_zlib_fname,
                                 self._import_json_dict,
                                 self._import_url),
                                (SourceTypes.BytesZlib,
                                 SourceTypes.FnamePlaintext,
                                 SourceTypes.FnameZlib,
                                 SourceTypes.DictJSON,
                                 SourceTypes.URL)
                                ):
            if src is not None:
                self._try_import(fxn, src, ())
                self.source_type = st
                return

    def data_file(self, *, expand=False, contract=False):
        """Generate a plaintext objects.txt as bytes."""
        # Rely on SuperDataObj to proof expand/contract args
        # Extra empty string at the end puts a newline at the end
        # of the generated string, consistent with files
        # generated by Sphinx.

        # Can't *-expand as a mixed argument in python 3.4, so have
        # to assemble the strings sequentially
        from itertools import chain

        striter = chain([self.header_preamble,
                         self.header_project.format(project=self.project),
                         self.header_version.format(version=self.version),
                         self.header_zlib],
                        (obj.data_line(expand=expand, contract=contract)
                         for obj in self.objects),
                        [''])

        return '\n'.join(striter).encode('utf-8')

    def suggest(self, name, *, thresh=50, with_index=False,
                with_score=False):
        """Suggest objects in the inventory to match a name."""
        import re
        import warnings

        # Suppress any UserWarning about the speed issue
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            from fuzzywuzzy import process as fwp

        # Must propagate list index to include in output
        # Search vals are rst prepended with list index
        srch_list = list('{0} {1}'.format(i, o) for i, o in
                         enumerate(self.objects_rst))

        # Composite each string result extracted by fuzzywuzzy
        # and its match score into a single string. The match
        # and score are returned together in a tuple.
        results = list('{0} {1}'.format(*_) for _ in
                       fwp.extract(name, srch_list, limit=None)
                       if _[1] >= thresh)

        # Define regex for splitting the three components, and
        # use it to convert composite result string to tuple:
        # (rst, score, index)
        p_idx = re.compile('^(\\d+)\\s+(.+?)\\s+(\\d+)$')
        results = list((m.group(2), int(m.group(3)), int(m.group(1)))
                       for m in map(p_idx.match, results))

        # Return based on flags
        if with_score:
            if with_index:
                return results
            else:
                return list(tup[:2] for tup in results)
        else:
            if with_index:
                return list(tup[::2] for tup in results)
            else:
                return list(tup[0] for tup in results)

    def _general_import(self):
        """Attempt sequence of all imports."""
        from zlib import error as ZlibError

        from jsonschema.exceptions import ValidationError

        # Lookups for method names and expected import-failure errors
        importers = {SourceTypes.BytesPlaintext: self._import_plaintext_bytes,
                     SourceTypes.BytesZlib: self._import_zlib_bytes,
                     SourceTypes.FnamePlaintext: self._import_plaintext_fname,
                     SourceTypes.FnameZlib: self._import_zlib_fname,
                     SourceTypes.DictJSON: self._import_json_dict,
                     }
        import_errors = {SourceTypes.BytesPlaintext: TypeError,
                         SourceTypes.BytesZlib: (ZlibError, TypeError),
                         SourceTypes.FnamePlaintext: (OSError,
                                                      TypeError),
                         SourceTypes.FnameZlib: (OSError,
                                                 TypeError,
                                                 ZlibError),
                         SourceTypes.DictJSON: (ValidationError),
                         }

        # Attempt series of import approaches
        # Enum keys are ordered, so iteration is too.
        for st in SourceTypes:
            if st not in importers:
                # No action for source types w/o a handler function defined.
                continue

            if self._try_import(importers[st], self._source,
                                import_errors[st]):
                self.source_type = st
                return

        # Nothing worked, complain.
        raise TypeError('Invalid Inventory source type')

    def _try_import(self, import_fxn, src, exc):
        """Attempt the indicated import method on the indicated source.

        Returns True on success.

        """
        try:
            p, v, o = import_fxn(src)
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
        objects.extend(gen_dataobjs())

        if len(objects) == 0:
            raise TypeError('No objects found in plaintext')

        return project, version, objects

    def _import_zlib_bytes(self, b_str):
        """Import a zlib-compressed inventory."""
        from .zlib import decompress

        b_plain = decompress(b_str)
        p, v, o = self._import_plaintext_bytes(b_plain)

        return p, v, o

    def _import_plaintext_fname(self, fn):
        """Import a plaintext inventory file."""
        from .fileops import readbytes

        b_plain = readbytes(fn)

        return self._import_plaintext_bytes(b_plain)

    def _import_zlib_fname(self, fn):
        """Import a zlib-compressed inventory file."""
        from .fileops import readbytes

        b_zlib = readbytes(fn)

        return self._import_zlib_bytes(b_zlib)

    def _import_url(self, url):
        """Import a file from a remote URL."""
        import urllib.request as urlrq

        import certifi

        # Caller's responsibility to ensure URL points
        # someplace safe/sane!
        resp = urlrq.urlopen(url, cafile=certifi.where())
        b_str = resp.read()

        # Plaintext URL D/L is unreliable; zlib only
        return self._import_zlib_bytes(b_str)

    def _import_json_dict(self, d):
        """Import flat-dict composited data."""
        import jsonschema

        from .data import DataObjStr
        from .schema import json_schema

        # Validate the dict against the schema. Schema
        # WILL allow an inventory with no objects here
        val = jsonschema.Draft4Validator(json_schema)
        val.validate(d)

        # Pull header items first
        project = d[HeaderFields.Project.value]
        version = d[HeaderFields.Version.value]
        count = d[HeaderFields.Count.value]

        # No objects is not allowed
        if count < 1:
            raise ValueError('Import of zero-length inventory')

        # Going to destructively process d, so shallow-copy it first
        d = d.copy()

        # Expecting the dict to be indexed by string integers
        objects = []
        for i in range(count):
            try:
                objects.append(DataObjStr(**d.pop(str(i))))
            except KeyError as e:
                if self._count_error:
                    err_str = ("Too few objects found in dict "
                               "(halt at {0}, expect {1})".format(i, count))
                    raise ValueError(err_str) from e

        # Complain if remaining objects are anything other than the
        # inventory-level metadata
        hf_values = set(e.value for e in HeaderFields)
        check_value = self._count_error and set(d.keys()).difference(hf_values)
        if check_value:
            # A truthy value here will be the contents
            # of the above set difference
            err_str = ("Too many objects in dict ({0})".format(check_value))
            raise ValueError(err_str)

        # Should be good to return
        return project, version, objects
