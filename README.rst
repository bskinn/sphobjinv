sphobjinv: Manipulate and inspect Sphinx objects.inv files
==========================================================

**Current Development Version:**

.. image:: https://img.shields.io/github/workflow/status/bskinn/sphobjinv/ci-tests?logo=github
    :alt: GitHub Workflow Status
    :target: https://github.com/bskinn/sphobjinv/actions

.. image:: https://codecov.io/gh/bskinn/sphobjinv/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/bskinn/sphobjinv

**Most Recent Stable Release:**

.. image:: https://img.shields.io/pypi/v/sphobjinv.svg?logo=pypi
    :target: https://pypi.org/project/sphobjinv

.. image:: https://img.shields.io/pypi/pyversions/sphobjinv.svg?logo=python

**Info:**

.. image:: https://img.shields.io/readthedocs/sphobjinv/latest.svg
    :target: http://sphobjinv.readthedocs.io/en/latest/

.. image:: https://badges.gitter.im/sphobjinv/community.svg
   :alt: Join the chat at https://gitter.im/sphobjinv/community
   :target: https://gitter.im/sphobjinv/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/bskinn/sphobjinv/blob/stable/LICENSE.txt

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://pepy.tech/badge/sphobjinv/month
    :target: https://pepy.tech/project/sphobjinv?versions=2.1b1&versions=2.2b1&versions=2.2&versions=2.1&versions=2.0.1

----

**Using Sphinx?**

**Having trouble writing cross-references?**

``sphobjinv`` (short for '**sph**\ inx **obj**\ ects.\ **inv**') can help!

The syntax required for a functional Sphinx cross-reference is highly
non-obvious in many cases. Sometimes Sphinx can guess correctly what
you mean, but it's pretty hit-or-miss.  The best approach is to provide
Sphinx with a completely specified cross-reference, and that's where
``sphobjinv`` comes in.

After a ``pip install sphobjinv`` (or ``pipx install sphobjinv``), find the
documentation set you want to cross-reference into, and pass it to
``sphobjinv suggest``.

For internal cross-references, locate ``objects.inv`` within ``build/html``::

    $ sphobjinv suggest doc/build/html/objects.inv as_rst -st 58

    Project: sphobjinv
    Version: 2.3

    219 objects in inventory.

    11 results found at/above current threshold of 58.

    Cannot infer intersphinx_mapping from a local objects.inv.

      Name                                                Score
    ---------------------------------------------------  -------
    :py:property:`sphobjinv.data.SuperDataObj.as_rst`      60
    :py:class:`sphobjinv.cli.parser.PrsConst`              59
    :py:class:`sphobjinv.data.DataFields`                  59
    :py:class:`sphobjinv.data.DataObjBytes`                59
    :py:class:`sphobjinv.data.DataObjStr`                  59
    :py:class:`sphobjinv.data.SuperDataObj`                59
    :py:class:`sphobjinv.enum.HeaderFields`                59
    :py:class:`sphobjinv.enum.SourceTypes`                 59
    :py:function:`sphobjinv.fileops.writebytes`            59
    :py:function:`sphobjinv.fileops.writejson`             59
    :py:class:`sphobjinv.inventory.Inventory`              59

.. end shell command

The ``-s`` argument in the above shell command indicates to print the
``fuzzywuzzy`` match score along with each search result, and ``-t 50``
changes the reporting threshold for the match score.

For external references, just find the API documentation wherever it lives on
the web, and pass ``sphobjinv suggest`` a URL from within the documentation set
with the ``--url/-u`` flag. For example, say I need to know how to
cross-reference the ``linspace`` function from numpy (see
`here <https://numpy.org/doc/1.23/reference/generated/numpy.linspace.html>`__)::

    $ sphobjinv suggest https://numpy.org/doc/1.23/reference/index.html linspace -su

    Attempting https://numpy.org/doc/1.23/reference/index.html ...
      ... no recognized inventory.
    Attempting "https://numpy.org/doc/1.23/reference/index.html/objects.inv" ...
      ... HTTP error: 404 Not Found.
    Attempting "https://numpy.org/doc/1.23/reference/objects.inv" ...
      ... HTTP error: 404 Not Found.
    Attempting "https://numpy.org/doc/1.23/objects.inv" ...
      ... inventory found.

    Project: NumPy
    Version: 1.23

    8074 objects in inventory.

    8 results found at/above current threshold of 75.

    The intersphinx_mapping for this docset is LIKELY:

      (https://numpy.org/doc/1.23/, None)


      Name                                                           Score
    --------------------------------------------------------------  -------
    :py:function:`numpy.linspace`                                     90
    :py:method:`numpy.polynomial.chebyshev.Chebyshev.linspace`        90
    :py:method:`numpy.polynomial.hermite.Hermite.linspace`            90
    :py:method:`numpy.polynomial.hermite_e.HermiteE.linspace`         90
    :py:method:`numpy.polynomial.laguerre.Laguerre.linspace`          90
    :py:method:`numpy.polynomial.legendre.Legendre.linspace`          90
    :py:method:`numpy.polynomial.polynomial.Polynomial.linspace`      90
    :std:doc:`reference/generated/numpy.linspace`                     90

.. end shell command

**NOTE** that the results from ``sphobjinv suggest`` are printed using the
longer *block directives*, whereas cross-references must be composed using the
*inline directives*. Thus, the above ``linspace()`` function must be
cross-referenced as ``:func:`numpy.linspace```, **not**
``:function:`numpy.linspace```.

**Need to edit an inventory after it's created, or compose one from scratch?**

``sphobjinv`` can help with that, too.

``objects.inv`` files can be decompressed to plaintext at the commandline::

    $ sphobjinv convert plain -o doc/build/html/objects.inv doc/scratch/
    Conversion completed.
    '...objects.inv' converted to '...objects.txt' (plain).

.. end shell command

JSON output is supported (``sphobjinv convert json ...``), and
inventories can be re-compressed to the
partially-zlib-compressed form that ``intersphinx`` reads
(``sphobjinv convert zlib ...``).

Alternatively, ``sphobjinv`` exposes an API to enable automation of
inventory creation/modification::

    >>> import sphobjinv as soi
    >>> inv = soi.Inventory('doc/build/html/objects.inv')
    >>> print(inv)
    <Inventory (fname_zlib): sphobjinv v2.3, 219 objects>
    >>> inv.project
    'sphobjinv'
    >>> inv.version
    '2.3'
    >>> inv.objects[0]
    DataObjStr(name='sphobjinv.cli.convert', domain='py', role='module', priority='0', uri='cli/implementation/convert.html#module-$', dispname='-')

The API also enables straightforward re-export of an inventory,
for subsequent use with ``intersphinx`` cross-references.
See `the docs <http://sphobjinv.readthedocs.io/en/latest/
api_usage.html#exporting-an-inventory>`__
for more details.

----

Full documentation is hosted at
`Read The Docs <http://sphobjinv.readthedocs.io/en/latest/>`__.

Available on `PyPI <https://pypi.org/project/sphobjinv>`__
(``pip install sphobjinv``).

Source on `GitHub <https://github.com/bskinn/sphobjinv>`__.  Bug reports
and feature requests are welcomed at the
`Issues <https://github.com/bskinn/sphobjinv/issues>`__ page there.

Copyright (c) Brian Skinn 2016-2022

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/sphobjinv/blob/main/LICENSE.txt>`__
for full license terms.
