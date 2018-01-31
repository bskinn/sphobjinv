r"""*Custom errors for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

.. note::

    Objects documented here MAY or MAY NOT be part of the official
    ``sphobjinv`` API.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    5 Nov 2017

**Copyright**
    \(c) Brian Skinn 2016-2018

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt| for full license terms

**Members**

"""


class SphobjinvError(Exception):
    """Custom ``sphobjinv`` error superclass."""


class VersionError(SphobjinvError):
    """Raised when attempting an operation on an unsupported version.

    The current version of ``sphobjinv`` only supports 'version 2'
    |objects.inv| files (see :doc:`here </syntax>`).

    """


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
