# ----------------------------------------------------------------------------
# Name:        data
# Purpose:     Objects.inv data manipulation for sphobjinv
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     7 Nov 2017
# Copyright:   (c) Brian Skinn 2016-2017
# License:     The MIT License; see "LICENSE.txt" for full license terms
#                   and contributor agreement.
#
#       This file is part of Sphinx Objects.inv Encoder/Decoder, a toolkit for
#       encoding and decoding objects.inv files for use with intersphinx.
#
#       http://www.github.com/bskinn/sphobjinv
#
# ----------------------------------------------------------------------------

"""Module for manipulation of objects.inv data."""

from abc import ABCMeta, abstractmethod
from enum import Enum

import attr


class DataFields(Enum):
    """Enum for the regex groups of objects.inv data items."""

    Name = 'name'
    Domain = 'domain'
    Role = 'role'
    Priority = 'priority'
    URI = 'uri'
    DispName = 'dispname'


class HeaderFields(Enum):
    """Enum for regex groups of objects.inv header data."""

    Project = 'project'
    Version = 'version'
    Count = 'count'
    Objects = 'objects'


def _utf8_decode(b):
    """Decode (if needed) to str."""
    if type(b) is bytes:
        return b.decode(encoding='utf-8')
    elif type(b) is str:
        return b
    else:
        raise TypeError("Argument must be 'bytes' or 'str'")


def _utf8_encode(s):
    """Encode (if needed) to bytes."""
    if type(s) is str:
        return s.encode(encoding='utf-8')
    elif type(s) is bytes:
        return s
    else:
        raise TypeError("Argument must be 'bytes' or 'str'")


class SuperDataObj(object, metaclass=ABCMeta):
    """Superclass defining common DataObj methods &c."""

    # These names must match the str values of the DataFields enum
    data_line_fmt = ('{name} {domain}:{role} {priority} '
                     '{uri} {dispname}')

    @property
    @abstractmethod
    def name(self):
        """Return object name."""
        pass

    @property
    @abstractmethod
    def domain(self):
        """Return object domain."""
        pass

    @property
    @abstractmethod
    def role(self):
        """Return object role."""
        pass

    @property
    @abstractmethod
    def priority(self):
        """Return object search priority."""
        pass

    @property
    @abstractmethod
    def uri(self):
        """Return object URI."""
        pass

    @property
    @abstractmethod
    def dispname(self):
        """Return object display name."""
        pass

    @property
    @abstractmethod
    def uri_abbrev(self):
        """Return char(s) for abbreviating URI tail."""
        pass

    @property
    @abstractmethod
    def dispname_abbrev(self):
        """Return char(s) for abbreviating display name."""
        pass

    @property
    @abstractmethod
    def as_str(self, s):
        """Return DataObjStr version of DataObj instance."""
        pass

    @property
    @abstractmethod
    def as_bytes(self, s):
        """Return DataObjBytes version of DataObj instance."""
        pass

    @abstractmethod
    def _data_line_postprocess(self, s):
        """Post-process the data_line chars output."""
        pass

    @property
    def uri_contracted(self):
        """Return contracted URI."""
        if self.uri.endswith(self.name):
            return self.uri[:-len(self.name)] + self.uri_abbrev
        else:
            return self.uri

    @property
    def uri_expanded(self):
        """Return expanded URI."""
        if self.uri.endswith(self.uri_abbrev):
            return self.uri[:-len(self.uri_abbrev)] + self.name
        else:
            return self.uri

    @property
    def dispname_contracted(self):
        """Return contracted display name."""
        if self.dispname == self.name:
            return self.dispname_abbrev
        else:
            return self.dispname

    @property
    def dispname_expanded(self):
        """Return expanded display name."""
        if self.dispname == self.dispname_abbrev:
            return self.name
        else:
            return self.dispname

    def flat_dict(self, *, expand=False, contract=False):
        """Return the object data formatted as a flat dict."""
        if expand and contract:
            raise ValueError("'expand' and 'contract' cannot "
                             "both be true.")

        d = {_: getattr(self, _) for _ in (__.value for __ in DataFields)}

        if expand:
            d.update({DataFields.URI.value: self.uri_expanded,
                      DataFields.DispName.value: self.dispname_expanded})

        if contract:
            d.update({DataFields.URI.value: self.uri_contracted,
                      DataFields.DispName.value: self.dispname_contracted})

        return d

    def update_struct_dict(self, d, *, expand=False, contract=False):
        """Update structured dict 'd' with the object data."""
        # Create a new dict with the leaf values. Invalid case of
        # expand == contract == True handled by flat_dict
        flat_d = self.flat_dict(expand=expand, contract=contract)
        new_d = {_: flat_d[_] for _ in
                 [DataFields.Priority.value,
                  DataFields.URI.value,
                  DataFields.DispName.value]}

        # Retrieve any existing domain dictionary, or create a new
        # empty dict
        d_domain = d.get(self.domain, {})

        if len(d_domain) > 0:
            # The domain already exists in d
            # Retrieve any existing role dict, or create a new
            # empty dict
            d_role = d_domain.get(self.role, {})

            # Either way, add the leaf data under the object name
            d_role.update({self.name: new_d})

            # If only one item now exists, must update the domain
            # dict with the newly created role dict
            if len(d_role) == 1:
                d_domain.update({self.role: d_role})

        else:
            # The domain doesn't exist in d
            # A role dict of necessity must be created new
            d_role = {self.name: new_d}

            # Add the new role dict to the new-empty domain dict
            d_domain.update({self.role: d_role})

            # Add the new domain dict to the input dict
            d.update({self.domain: d_domain})

        # No return

    def data_line(self, *, expand=False, contract=False):
        """Compose objects.txt data line from instance contents."""
        # Rely on .flat_dict to check for invalid expand == contract == True
        fmt_d = self.as_str.flat_dict(expand=expand, contract=contract)

        retval = self.data_line_fmt.format(**fmt_d)

        return self._data_line_postprocess(retval)


@attr.s(slots=True, frozen=True)
class DataObjStr(SuperDataObj):
    """Container for string versions of objects.inv data."""

    uri_abbrev = '$'
    dispname_abbrev = '-'

    name = attr.ib(convert=_utf8_decode)
    domain = attr.ib(convert=_utf8_decode)
    role = attr.ib(convert=_utf8_decode)
    priority = attr.ib(convert=_utf8_decode)
    uri = attr.ib(convert=_utf8_decode)
    dispname = attr.ib(convert=_utf8_decode)

    as_bytes = attr.ib(repr=False)

    @as_bytes.default
    def _as_bytes_default(self):
        return DataObjBytes(name=self.name,
                            domain=self.domain,
                            role=self.role,
                            priority=self.priority,
                            uri=self.uri,
                            dispname=self.dispname,
                            as_str=self)

    as_str = attr.ib(repr=False)

    @as_str.default
    def _as_str_default(self):
        return self

    def _data_line_postprocess(self, s):
        """Perform no postprocessing."""
        return s


@attr.s(slots=True, frozen=True)
class DataObjBytes(SuperDataObj):
    """Container for the data for an objects.inv entry."""

    uri_abbrev = b'$'
    dispname_abbrev = b'-'

    name = attr.ib(convert=_utf8_encode)
    domain = attr.ib(convert=_utf8_encode)
    role = attr.ib(convert=_utf8_encode)
    priority = attr.ib(convert=_utf8_encode)
    uri = attr.ib(convert=_utf8_encode)
    dispname = attr.ib(convert=_utf8_encode)

    as_str = attr.ib(repr=False)

    @as_str.default
    def _as_str_default(self):
        return DataObjStr(name=self.name,
                          domain=self.domain,
                          role=self.role,
                          priority=self.priority,
                          uri=self.uri,
                          dispname=self.dispname,
                          as_bytes=self)

    as_bytes = attr.ib(repr=False)

    @as_bytes.default
    def _as_bytes_default(self):
        return self

    def _data_line_postprocess(self, s):
        """Encode to bytes before data_line return."""
        return s.encode('utf-8')


@attr.s(slots=True, cmp=False)
class Inventory(object):
    """Entire contents of an objects.inv inventory.

    All information stored within as str, even if imported
    from a bytes source.

    """

    from copy import deepcopy as _deepcopy

    _source = attr.ib(repr=False, convert=_deepcopy)
    project = attr.ib(init=False, default=None)
    version = attr.ib(init=False, default=None)
    objects = attr.ib(init=False, default=attr.Factory(list))

    @property
    def count(self):
        """Return the number of objects currently in inventory."""
        return len(self.objects)

    def __str__(self):
        """Return concise, readable description of contents."""
        return "<Inventory: {0} v{1}, {2} objects>".format(self.project,
                                                           self.version,
                                                           self.count)

    def __attrs_post_init__(self):
        """Construct the inventory from the indicated source."""
        # Leave uninitialized if _source is None
        if self._source is None:
            return

        # Attempt series of import types
        if self._try_import(self._import_plaintext_bytes, TypeError):
            return

        # Nothing worked, complain.
        raise TypeError('Invalid Inventory source type')

    def _try_import(self, import_fxn, exc):
        """Attempt the indicated import method.

        Returns True on success.

        """
        try:
            import_fxn(self._source)
        except exc:
            return False

        return True

    def _import_plaintext_bytes(self, b_str):
        """Import an inventory from plaintext bytes."""
        from .re import pb_data, pb_project, pb_version

        b_res = pb_project.search(b_str).group(HeaderFields.Project.value)
        self.project = b_res.decode('utf-8')

        b_res = pb_version.search(b_str).group(HeaderFields.Version.value)
        self.version = b_res.decode('utf-8')

        def gen_dataobjs():
            for mch in pb_data.finditer(b_str):
                yield DataObjStr(**mch.groupdict())

        list(map(self.objects.append, gen_dataobjs()))


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
