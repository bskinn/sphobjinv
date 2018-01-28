.. API page

API
===

The primary ``sphobjinv`` API consists of two pairs of functions:

 * :func:`~sphobjinv.fileops.readfile` /
   :func:`~sphobjinv.fileops.writefile` -- Read/write files from/to disk
   as |bytes|, for proper behavior of :mod:`zlib` (de)compression.

 * :func:`~sphobjinv.zlib.encode` /
   :func:`~sphobjinv.zlib.decode` -- Encode/decode the object data
   read from disk.

Also exposed are two |re.compile| patterns, potentially useful in parsing
**decoded data only**\ :

 * :data:`~sphobjinv.re.p_comments` -- Retrieves the
   `#`\ -prefixed comment lines

 * :data:`~sphobjinv.re.p_data` -- Retrieves all lines
   not prefixed by `#`


The normal workflow would be:

 #. Import the module; e.g.::

        >>> import sphobjinv as soi

 #. Read the desired file data (compressed or uncompressed) with
    :func:`~sphobjinv.fileops.readfile`::

        >>> fd = soi.readfile('/path/to/file')

 #. Decode [or encode] the file data with :func:`~sphobjinv.zlib.decode`
    [or :func:`~sphobjinv.zlib.encode`]::

        >>> data = soi.decode(fd)

 #. Write the desired file with :func:`~sphobjinv.fileops.writefile`,
    or otherwise use the resulting |bytes| data::

        >>> len(soi.p_data.findall(data))   # e.g., retrieve the number of object entries
        6319

        >>> soi.writefile('/path/to/new/file', data)


**Members**

.. automodule:: sphobjinv.fileops
    :members:
    :noindex:

.. automodule:: sphobjinv.zlib
    :members:
    :noindex:

.. automodule:: sphobjinv.re
    :members:
    :noindex:


**Detailed Module Info (not formal API)**

.. toctree::
    :maxdepth: 1

    modules/re
