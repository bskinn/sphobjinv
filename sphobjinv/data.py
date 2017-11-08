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
    return b.decode(encoding='utf-8')


@attr.s(slots=True)
class DataAsStr(object):
    """Container for string versions of objects.inv data."""
    name = attr.ib(convert=_utf8_decode)
    domain = attr.ib(convert=_utf8_decode)
    role = attr.ib(convert=_utf8_decode)
    priority = attr.ib(convert=_utf8_decode)
    uri = attr.ib(convert=_utf8_decode)
    dispname = attr.ib(convert=_utf8_decode)


@attr.s(slots=True)
class DataObject(object):
    """Container for the data for an objects.inv entry."""

    name = attr.ib(validator=attr.validators.instance_of(bytes))
    domain = attr.ib(validator=attr.validators.instance_of(bytes))
    role = attr.ib(validator=attr.validators.instance_of(bytes))
    priority = attr.ib(validator=attr.validators.instance_of(bytes))
    uri = attr.ib(validator=attr.validators.instance_of(bytes))
    dispname = attr.ib(validator=attr.validators.instance_of(bytes))

    as_str = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        self.as_str = DataAsStr(name=self.name,
                            domain=self.domain,
                            role=self.role,
                            priority=self.priority,
                            uri=self.uri,
                            dispname=self.dispname)

    def dict_flat_bytes(self):
        return {_: getattr(self, _)
                for _ in (__.value for __ in DataFields)}

    def dict_flat_strs(self):
        return {_: getattr(self.as_str, _)
                for _ in (__.value for __ in DataFields)}

    def update_struct_dict_bytes(self, d):
        # Create a new dict with the leaf values
        new_d = dict({})
        new_d.update({b'priority': self.priority,
                      b'uri': self.uri,
                      b'dispname': self.dispname})

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


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
