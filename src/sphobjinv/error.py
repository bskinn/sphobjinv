r"""*Custom errors for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    5 Nov 2017

**Copyright**
    \(c) Brian Skinn 2016-2022

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""


class SphobjinvError(Exception):
    """Custom ``sphobjinv`` error superclass."""


class VersionError(SphobjinvError):
    """Raised when attempting an operation on an unsupported version.

    The current version of ``sphobjinv`` only supports 'version 2'
    |objects.inv| files (see :doc:`here </syntax>`).

    """

    # TODO: Add SOI prefix to this class name as part of the exceptions refactor


class SOIIntersphinxError(SphobjinvError):
    """Family of errors from the sphobjinv.intersphinx module."""


class SOIIsphxNotASuffixError(SOIIntersphinxError):
    """Raised when a non-suffix URI is passed to the function matching."""

    def __init__(self, *args, base, suffix, **kwargs):
        """Initialize the instance with base and suffix strings."""
        super().__init__(*args, **kwargs)
        self.base = base
        self.suffix = suffix

    def __str__(self):
        """Provide human-readable exception message."""
        return f"'{self.suffix}' is not a suffix of '{self.base}'"
