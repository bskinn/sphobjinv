r"""``sphobjinv`` *data class for full inventories*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

.. note::

    Objects documented here MAY or MAY NOT be part of the official
    ``sphobjinv`` :doc:`API </api/formal>`.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    7 Dec 2017

**Copyright**
    \(c) Brian Skinn 2016-2018

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from enum import Enum

import attr

from .data import DataObjStr


class HeaderFields(Enum):
    """|Enum| for various inventory-level data items.

    A subset of these |Enum| values is used in various Regex,
    JSON, and string formatting contexts within :class:`Inventory`
    and :data:`schema.json_schema <sphobjinv.schema.json_schema>`.

    """

    #: Project name associated with an inventory
    Project = 'project'

    #: Project version associated with an inventory
    Version = 'version'

    #: Number of objects contained in the inventory
    Count = 'count'

    #: The |str| value of this |Enum| member is accepted as a root-level
    #: key in a |dict| to be imported into an :class:`Inventory`.
    #: The corresponding value in the |dict| may contain any arbitrary data.
    #: Its possible presence is accounted for in
    #: :data:`schema.json_schema <sphobjinv.schema.json_schema>`.
    #:
    #: The data associated with this key are **ignored**
    #: during import into an :class:`Inventory`.
    Metadata = 'metadata'


class SourceTypes(Enum):
    """|Enum| for the import mode used in instantiating an |Inventory|.

    Since |Enum| keys iterate in definition order, the
    definition order here defines the order in which |Inventory|
    objects attempt to parse a source object passed to
    :meth:`Inventory.__init__` either as a positional argument
    or via the generic `source` keyword argument.

    This order **DIFFERS** from the documentation order, which is
    alphabetical.

    """

    #: No source; |Inventory| was instantiated with
    #: :data:`~Inventory.project` and :data:`~Inventory.version`
    #: as empty strings and
    #: :data:`~Inventory.objects` as an empty |list|.
    Manual = 'manual'

    #: Instantiation from a plaintext |objects.inv| |bytes|.
    BytesPlaintext = 'bytes_plain'

    #: Instantiation from a zlib-compressed
    #: |objects.inv| |bytes|.
    BytesZlib = 'bytes_zlib'

    #: Instantiation from a plaintext |objects.inv| file on disk.
    FnamePlaintext = 'fname_plain'

    #: Instantiation from a zlib-compressed |objects.inv| file on disk.
    FnameZlib = 'fname_zlib'

    #: Instantiation from a |dict| validated against
    #: :data:`schema.json_schema <sphobjinv.schema.json_schema>`.
    DictJSON = 'dict_json'

    #: Instantiation from a zlib-compressed |objects.inv| file
    #: downloaded from a URL.
    URL = 'url'


@attr.s(slots=True, cmp=False)
class Inventory(object):
    r"""Entire contents of an |objects.inv| inventory.

    All information is stored internally as |str|,
    even if imported from a |bytes| source.

    All arguments except `count_error` are used to specify the source
    from which the |Inventory| contents are to be populated.
    **At most ONE** of these source arguments may be other than |None|.

    The `count_error` argument is only relevant to the `dict_json` source type.

    `source`

        The |Inventory| will attempt to parse the indicated
        source object as each of the below types in sequence,
        **except** for `url`.

        This argument is included mainly as a convenience
        feature for use in interactive sessions, as
        invocations of the following form implicitly
        populate `source`, as the first positional argument::

            >>> inv = Inventory(src_obj)

        In most cases, for clarity it is recommended
        that programmatic instantiation of |Inventory| objects
        utilize the below format-specific arguments.

    `plaintext`

        Object is to be parsed as the |bytes|
        plaintext contents of an |objects.inv| inventory.

    `zlib`

        Object is to be parsed as the |bytes|
        zlib-compressed contents of an
        |objects.inv| inventory.

    `fname_plain`

        Object is the |str| path to a file containing
        the plaintext contents of an |objects.inv| inventory.

    `fname_zlib`

        Object is the |str| path to a file containing
        the zlib-compressed contents of an
        |objects.inv| inventory.

    `dict_json`

        Object is a |dict| containing the contents
        of an |objects.inv| inventory, conforming to
        the JSON schema of
        :data:`schema.json_schema <sphobjinv.schema.json_schema>`.

        If `count_error` is passed as |True|,
        then a :exc:`ValueError` is raised if
        the number of objects found in the |dict|
        does not match the value associated with
        its `count` key.
        If `count_error` is passed as |False|,
        an object count mismatch is ignored.

    `url`

        Object is a |str| URL to a zlib-compressed
        |objects.inv| file.
        Any URL type supported by
        :mod:`urllib.request` SHOULD work; only
        |cour|\ http:\ |/cour| and
        |cour|\ file:\ |/cour|
        have been directly tested, however.

        No authentication is supported at this time.

    **Members**

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
        # valid inventory-level header keys
        hf_values = set(e.value for e in HeaderFields)
        check_value = self._count_error and set(d.keys()).difference(hf_values)
        if check_value:
            # A truthy value here will be the contents
            # of the above set difference
            err_str = ("Too many objects in dict ({0})".format(check_value))
            raise ValueError(err_str)

        # Should be good to return
        return project, version, objects


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
