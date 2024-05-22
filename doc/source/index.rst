.. Sphinx Objects.inv Converter documentation master file, created by
   sphinx-quickstart on Wed May 18 22:42:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to sphobjinv!
=====================

*A toolkit for inspection/manipulation of Sphinx objects inventories*


When documentation is built using, e.g., Sphinx's :obj:`~sphinx.builders.html.StandaloneHTMLBuilder`,
an inventory of the named objects in the documentation set `is dumped
<https://github.com/sphinx-doc/sphinx/blob/adde25689377b58791ad2e357817378ad3a08a1b/sphinx/util/inventory.py#L158-L189>`__
to a file called |objects.inv| in the html build directory.
(One common location is, |cour|\ doc/build/html\ |/cour|, though the exact location will vary
depending on the details of how Sphinx is configured.)  This file is read by |isphx| when
generating links in other documentation.

Since version 1.0 of Sphinx (~July 2010), the data in these |objects.inv| inventories is compressed by
:mod:`zlib` (presumably to reduce storage requirements and improve download speeds; "version 2"),
whereas prior to that date the data was left uncompressed ("version 1").  This compression renders
the files non-human-readable.  **It is the purpose of this package to enable quick and simple
compression/decompression and inspection of these "version 2" inventory files.**

In particular, |soi| was developed to satisfy two primary use cases:

 #. Searching and inspection of |objects.inv| contents in order to identify
    how to properly construct |isphx| references. |br| |br|

 #. Assembly of new |objects.inv| files in order to allow |isphx| cross-referencing
    of other documentation sets that were not created by Sphinx.

For more background on the mechanics of the Sphinx data model and
Sphinx cross-references generally, see
`this talk <https://www.youtube.com/watch?v=CfInPYkbTZE>`__ from PyOhio 2019.

----

Install |soi| via |cour|\ pip\ |/cour|::

    $ pip install sphobjinv

Or, if you only plan to use the |soi| CLI, another option is |pipx|_::

    $ pipx install sphobjinv

As of Nov 2022, |soi| is also available via conda-forge. After activating the desired conda environment::

    $ conda install -c conda-forge sphobjinv

Alternatively, |soi| is packaged with
`multiple POSIX distributions <https://repology.org/projects/?search=sphobjinv>`__
and package managers, including:

  * Alpine Linux: ``py3-sphobjinv`` (`info <https://pkgs.alpinelinux.org/packages?name=py3-sphobjinv>`__)

  * Arch Linux: ``python-sphobjinv``

  * Fedora: ``python-sphobjinv`` (`info <https://src.fedoraproject.org/rpms/python-sphobjinv>`__)

  * Gentoo: ``dev-python/sphobjinv`` (`info <https://gitweb.gentoo.org/repo/gentoo.git/tree/dev-python/sphobjinv>`__)

  * Guix: ``python-sphobjinv``

  * Manjaro: ``python-sphobjinv``

  * OpenEuler: ``python-sphobjinv``

  * openSUSE: ``python-sphobjinv`` (`info <https://build.opensuse.org/package/show/openSUSE:Factory/python-sphobjinv>`__)

  * Parabola: ``python-sphobjinv`` (`info <https://www.parabola.nu/packages/?q=python-sphobjinv>`__)

  * pkgsrc: ``textproc/py-sphobjinv`` (`info <https://pkgsrc.se/textproc/py-sphobjinv>`__)

  * spack: ``py-sphobjinv``


|soi| is configured for use both as a
:doc:`command-line script <cli/index>` and as a
:doc:`Python package <api_usage>`.

The optional dependency |python-Levenshtein|_ for accelerating
the "suggest" functionality is no longer available due to a
licensing conflict, and has been deprecated. See
:doc:`here <levenshtein>` for more information.

The project source repository is on GitHub: `bskinn/sphobjinv
<https://github.com/bskinn/sphobjinv>`__.



.. toctree::
   :maxdepth: 1
   :hidden:

   cli/index
   api_usage
   customfile
   levenshtein
   syntax
   api/index
   CLI Implementation (non-API) <cli/implementation/index>



Indices and Tables
------------------

:ref:`genindex` --- :ref:`modindex` --- :ref:`search`
