.. API page

API
===

The primary ``sphobjinv`` API consists of two pairs of functions:

 * :func:`~sphobjinv.sphobjinv.readfile` / 
   :func:`~sphobjinv.sphobjinv.writefile` -- Read/write files from/to disk
   as |bytes|, for proper behavior of :mod:`zlib` (de)compression.

 * :func:`~sphobjinv.sphobjinv.encode` / 
   :func:`~sphobjinv.sphobjinv.decode` -- Encode/decode the object data 
   read from disk.

Also exposed are two |re.compile| patterns, potentially useful in parsing
**decoded data only**\ :

 * :data:`~sphobjinv.sphobjinv.p_comments` -- Retrieves the 
   `#`\ -prefixed comment lines

 * :data:`~sphobjinv.sphobjinv.p_data` -- Retrieves all lines 
   not prefixed by `#`


The normal workflow would be:

 #. Import the module; e.g.::

        >>> import sphobjinv as soi

 #. Read the desired file data (compressed or uncompressed) with 
    :func:`~sphobjinv.sphobjinv.readfile`::

        >>> fd = soi.readfile('/path/to/file')

 #. Decode [or encode] the file data with :func:`~sphobjinv.sphobjinv.decode`
    [or :func:`~sphobjinv.sphobjinv.encode`]::

        >>> data = soi.decode(fd)

 #. Write the desired file with :func:`~sphobjinv.sphobjinv.writefile`, 
    or otherwise use the resulting |bytes| data::

        >>> len(soi.p_data.findall(data))   # e.g., retrieve the number of object entries
        6319

        >>> soi.writefile('/path/to/new/file', data)


**Members**

.. automodule:: sphobjinv.sphobjinv
    :members:

