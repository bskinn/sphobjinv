.. Sphinx Objects.inv Converter documentation master file, created by
   sphinx-quickstart on Wed May 18 22:42:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sphinx Objects.inv Encoder/Decoder
==================================

When documentation is built using, e.g., Sphinx's :obj:`~sphinx.builders.html.StandaloneHTMLBuilder`,
an inventory of the named objects in the documentation set `is dumped
<https://github.com/sphinx-doc/sphinx/blob/b371312887869c52e7be9033e60450a9dc12ca0c/sphinx/util/inventory.py#L159-L191>`__
to a file called |objects.inv| in the html build directory.  This file is read by |isphx| when
generating links in other documentation.

Since version 1.0 of Sphinx (~July 2010), the data in these |objects.inv| inventories is compressed by
:mod:`zlib` (presumably to reduce storage requirements and improve download speeds; "version 2"),
whereas prior to that date the data was left uncompressed ("version 1").  This compression renders
the files non-human-readable.  **It is the purpose of this package to enable quick and simple
compression/decompression and inspection of these files.**

In particular, |soi| was developed to satisfy two primary use cases:

 #. Searching and inspection of |objects.inv| contents in order to identify
    how to properly construct |isphx| references. |br| |br|

 #. Assembly of new |objects.inv| files in order to allow |isphx| cross-referencing
    of other documentation sets that were not created by Sphinx.

----

Sphinx Objects.inv Encoder/Decoder is available on PyPI under |soi|::

    pip install sphobjinv

The package is configured for use both as a
:doc:`command-line script <cmdline_usage>` and as a
:doc:`Python package <api_usage>`.

Installing the optional dependency |python-Levenshtein|_ substantially
accelerates the the "suggest" functionality; see
:doc:`here <levenshtein>` for more information.

The project source repository is on GitHub: `bskinn/sphobjinv
<https://www.github.com/bskinn/sphobjinv>`__.


.. Contents
.. --------

.. toctree::
   :maxdepth: 1
   :hidden:

   cmdline_usage
   api_usage
   customfile
   levenshtein
   syntax
   api_listing
   CLI Implementation (non-API) <modules/cmdline>



Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

