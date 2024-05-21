## sphobjinv: Manipulate and inspect Sphinx objects.inv files


#### Current Development Version

[![GitHub Workflow Status][workflow badge]][workflow link target]
[![Codecov Coverage][codecov badge]][codecov target]

#### Most Recent Stable Release

[![PyPI Version][pypi badge]][pypi link target]
![Python Versions][python versions badge]

#### Info

[![ReadTheDocs status][readthedocs badge]][readthedocs link target]
[![gitter chat][gitter badge]][gitter link target]

[![MIT License][license badge]][license link target]
[![black formatted][black badge]][black link target]
[![PePY stats][pepy badge]][pepy link target]

----

### Using Sphinx?

#### Having trouble writing cross-references?

`sphobjinv` (short for '**sph**inx **obj**ects.**inv**') can help!

The syntax required for a functional Sphinx cross-reference is highly
non-obvious in many cases. Sometimes Sphinx can guess correctly what
you mean, but it's pretty hit-or-miss.  The best approach is to provide
Sphinx with a completely specified cross-reference, and that's where
`sphobjinv` comes in.

After a `pip install sphobjinv` (or `pipx install sphobjinv`), find the
documentation set you want to cross-reference into, and pass it to
`sphobjinv suggest`.

For internal cross-references, locate `objects.inv` within `build/html`:

```none
$ sphobjinv suggest doc/build/html/objects.inv as_rst -st 58

------------------------------------------------

Cannot infer intersphinx_mapping from a local objects.inv.

------------------------------------------------

Project: sphobjinv
Version: 2.3

220 objects in inventory.

------------------------------------------------

11 results found at/above current threshold of 58.


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
```

The `-s` argument in the above shell command indicates to print the
`fuzzywuzzy` match score along with each search result, and `-t 50`
changes the reporting threshold for the match score.

For external references, find the API documentation wherever it lives on
the web, and pass `sphobjinv suggest` a URL from within the documentation set
with the `--url/-u` flag. For example, say I need to know how to
cross-reference the `linspace` function from numpy (see
[here][numpy linspace]):

```none
$ sphobjinv suggest https://numpy.org/doc/1.26/reference/index.html linspace -su

Attempting https://numpy.org/doc/1.26/reference/index.html ...
  ... no recognized inventory.
Attempting "https://numpy.org/doc/1.26/reference/index.html/objects.inv" ...
  ... HTTP error: 404 Not Found.
Attempting "https://numpy.org/doc/1.26/reference/objects.inv" ...
  ... HTTP error: 404 Not Found.
Attempting "https://numpy.org/doc/1.26/objects.inv" ...
  ... inventory found.

----------------------------------------------------------------------------------

The intersphinx_mapping for this docset is LIKELY:

  (https://numpy.org/doc/1.26/, None)

----------------------------------------------------------------------------------

Project: NumPy
Version: 1.26

8152 objects in inventory.

----------------------------------------------------------------------------------

8 results found at/above current threshold of 75.

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
```

**NOTE** that the results from `sphobjinv suggest` are printed using the
longer *block directives*, whereas cross-references must be composed using the
*inline directives*. Thus, the above `linspace()` function must be
cross-referenced as ``` :func:`numpy.linspace` ``` , **not**
``` :function:`numpy.linspace` ```.

**Need to edit an inventory after it's created, or compose one from scratch?**

`sphobjinv` can help with that, too.

`objects.inv` files can be decompressed to plaintext at the commandline:

```none
$ sphobjinv convert plain -o doc/build/html/objects.inv doc/scratch/
Conversion completed.
'...objects.inv' converted to '...objects.txt' (plain).
```

JSON output is supported (`sphobjinv convert json ...`), and
inventories can be re-compressed to the
partially-zlib-compressed form that `intersphinx` reads
(`sphobjinv convert zlib ...`).

Alternatively, `sphobjinv` exposes an API to enable automation of
inventory creation/modification:

```python
>>> import sphobjinv as soi
>>> inv = soi.Inventory('doc/build/html/objects.inv')
>>> print(inv)
<Inventory (fname_zlib): sphobjinv v2.3, 220 objects>
>>> inv.project
'sphobjinv'
>>> inv.version
'2.3'
>>> inv.objects[0]
DataObjStr(name='sphobjinv.cli.convert', domain='py', role='module', priority='0', uri='cli/implementation/convert.html#module-$', dispname='-')

```

The API also enables straightforward re-export of an inventory, for subsequent
use with `intersphinx` cross-references. See [the docs][soi docs inv export] for
more details.

----

Full documentation is hosted at [Read The Docs][readthedocs link target].

Available on [PyPI][pypi link target] (`pip install sphobjinv`).

Source on [GitHub][github repo]. Bug reports and feature requests are welcomed
at the [Issues][github issue tracker] page there.

Copyright (c) Brian Skinn 2016-2024

The `sphobjinv` documentation (including docstrings and README) is licensed
under a [Creative Commons Attribution 4.0 International License][cc-by 4.0]
(CC-BY). The `sphobjinv` codebase is released under the [MIT License]. See
[`LICENSE.txt`][license link target] for full license terms.


[black badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black link target]: https://github.com/psf/black
[cc-by 4.0]: http://creativecommons.org/licenses/by/4.0/
[codecov badge]: https://codecov.io/gh/bskinn/sphobjinv/branch/main/graph/badge.svg
[codecov target]: https://codecov.io/gh/bskinn/sphobjinv
[soi docs inv export]: http://sphobjinv.readthedocs.io/en/latest/api_usage.html#exporting-an-inventory
[github issue tracker]: https://github.com/bskinn/sphobjinv/issues
[github repo]: https://github.com/bskinn/sphobjinv
[gitter badge]: https://badges.gitter.im/sphobjinv/community.svg
[gitter link target]: https://gitter.im/sphobjinv/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
[license badge]: https://img.shields.io/github/license/mashape/apistatus.svg
[license link target]: https://github.com/bskinn/sphobjinv/blob/stable/LICENSE.txt
[mit license]: https://opensource.org/licenses/MIT
[numpy linspace]: https://numpy.org/doc/1.26/reference/generated/numpy.linspace.html
[pepy badge]: https://pepy.tech/badge/sphobjinv/month
[pepy link target]: https://pepy.tech/project/sphobjinv?versions=2.0.1&versions=2.1&versions=2.2.2&versions=2.3&versions=2.3.1
[pypi badge]: https://img.shields.io/pypi/v/sphobjinv.svg?logo=pypi]
[pypi link target]: https://pypi.org/project/sphobjinv
[python versions badge]: https://img.shields.io/pypi/pyversions/sphobjinv.svg?logo=python
[readthedocs badge]: https://img.shields.io/readthedocs/sphobjinv/latest.svg
[readthedocs link target]: http://sphobjinv.readthedocs.io/en/latest/
[workflow badge]: https://img.shields.io/github/actions/workflow/status/bskinn/sphobjinv/ci_tests.yml?logo=github&branch=main
[workflow link target]: https://github.com/bskinn/sphobjinv/actions
