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

import attr

from .re import DataFields


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


class SuperDataObj(object):
    """Superclass defining common DataObj methods &c."""

    def flat_dict(self):
        """Return the object data formatted as a flat dict."""
        return {_: getattr(self, _)
                for _ in (__.value for __ in DataFields)}

    def update_struct_dict(self, d):
        """Update structured dict 'd' with the object data."""
        # Create a new dict with the leaf values
        new_d = dict({})
        new_d.update({DataFields.Priority.value: self.priority,
                      DataFields.URI.value: self.uri,
                      DataFields.DispName.value: self.dispname})

        # Retrieve any existing domain dictionary, or create a new
        # empty dict
        d_domain = d.get(self.domain, dict({}))

        if len(d_domain) > 0:
            # The domain already exists in d
            # Retrieve any existing role dict, or create a new
            # empty dict
            d_role = d_domain.get(self.role, dict({}))

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


@attr.s(slots=True, frozen=True)
class DataObjStr(SuperDataObj):
    """Container for string versions of objects.inv data."""

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
                            as_str=None)


@attr.s(slots=True, frozen=True)
class DataObjBytes(SuperDataObj):
    """Container for the data for an objects.inv entry."""

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
                          as_bytes=None)


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
