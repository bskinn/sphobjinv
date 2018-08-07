sphobjinv: Manipulate and inspect Sphinx objects.inv files
==========================================================

**Current Development Version:**

.. image:: https://travis-ci.org/bskinn/sphobjinv.svg?branch=dev
    :target: https://travis-ci.org/bskinn/sphobjinv

.. image:: https://codecov.io/gh/bskinn/sphobjinv/branch/dev/graph/badge.svg
    :target: https://codecov.io/gh/bskinn/sphobjinv

**Most Recent Stable Release:**

.. image:: https://img.shields.io/pypi/v/sphobjinv.svg
    :target: https://pypi.org/project/sphobjinv

.. image:: https://img.shields.io/pypi/pyversions/sphobjinv.svg

**Info:**

.. image:: https://img.shields.io/readthedocs/sphobjinv/latest.svg
    :target: http://sphobjinv.readthedocs.io/en/latest/

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/bskinn/sphobjinv/blob/master/LICENSE.txt

----

**Using Sphinx?**

**Having trouble writing cross-references?**

``sphobjinv`` (short for '**sph**\ inx **obj**\ ects.\ **inv**') can help!

The syntax required for a functional Sphinx cross-reference is highly
non-obvious in many cases. Sometimes Sphinx can guess correctly what
you mean, but it's pretty hit-or-miss.  The best approach is to provide
Sphinx with a completely specified cross-reference, and that's where
``sphobjinv`` comes in.

After a ``pip install sphobjinv``, find the documentation set you want
to cross-reference into, and pass it to ``sphobjinv suggest``.

For internal cross-references, locate ``objects.inv`` within `build/html`::

    $ sphobjinv suggest doc/build/html/objects.inv as_rst -sit 50

      Name                                                        Score    Index
    -----------------------------------------------------------  -------  -------
    :py:attribute:`sphobjinv.data.SuperDataObj.as_rst`             60       56
    :py:function:`sphobjinv.cmdline.getparser`                     50       32
    :py:attribute:`sphobjinv.data.SuperDataObj.as_str`             50       57
    :py:attribute:`sphobjinv.inventory.Inventory.objects_rst`      50       99

.. end shell command

For external references, just find the documentation wherever it lives on the web,
and pass ``sphobjinv suggest`` a URL from within the documentation set
with the ``--url/-u`` flag. For example, say I need to know how to
cross-reference the ``redirect()`` function from Flask (see
`here <http://flask.pocoo.org/docs/1.0/api/?highlight=redirect#flask.redirect>`__)::

    $ sphobjinv suggest http://flask.pocoo.org/docs/1.0/views/#method-hints redirect -siu

    No inventory at provided URL.
    Attempting "http://flask.pocoo.org/docs/1.0/views/objects.inv" ...
    Attempting "http://flask.pocoo.org/docs/1.0/objects.inv" ...
    Remote inventory found.

      Name                            Score    Index
    -------------------------------  -------  -------
    :py:function:`flask.redirect`      90       360

.. end shell command

**NOTE** that the results from ``sphobjinv suggest`` are printed using the longer
*block directives*, whereas cross-references must be composed using the
*inline directives*. Thus, the above ``redirect()`` function must be
cross-referenced as ``:func:`flask.redirect```, **not**
``:function:`flask.redirect```.

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
    <Inventory (fname_zlib): sphobjinv v2.0, 179 objects>
    >>> inv.project
    'sphobjinv'
    >>> inv.version
    '2.0'
    >>> inv.objects[0]
    DataObjStr(name='sphobjinv.cmdline', domain='py', role='module', priority='0', uri='cli/implementation.html#module-$', dispname='-')

The API also enables straightforward re-export of an inventory,
for subsequent use with ``intersphinx`` cross-references.
See `the docs <http://sphobjinv.readthedocs.io/en/latest/>`__
for more details.

----

Full documentation is hosted at
`Read The Docs <http://sphobjinv.readthedocs.io/en/latest/>`__.

Available on `PyPI <https://pypi.python.org/pypi/sphobjinv>`__
(``pip install sphobjinv``).

Source on `GitHub <https://github.com/bskinn/sphobjinv>`__.  Bug reports
and feature requests are welcomed at the
`Issues <https://github.com/bskinn/sphobjinv/issues>`__ page there.

Copyright (c) Brian Skinn 2016-2018

License: The MIT License. See `LICENSE.txt <https://github.com/bskinn/sphobjinv/blob/master/LICENSE.txt>`__
for full license terms.
