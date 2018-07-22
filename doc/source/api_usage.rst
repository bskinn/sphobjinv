.. API usage page

API Usage
=========

In all of the below, the |soi| package has been imported as
|cour|\ soi\ |/cour|, and the working temp directory has
been populated with the |cour|\ objects_attrs.inv\ |/cour| inventory.

Inspecting an Inventory
-----------------------

Inspecting the contents of an existing inventory is handled entirely by the
:class:`~sphobjinv.inventory.Inventory` class:

.. doctest:: api_inspect

    >>> inv = soi.Inventory('objects_attrs.inv')
    >>> print(inv)
    <Inventory (fname_zlib): attrs v17.2, 56 objects>
    >>> inv.version
    '17.2'
    >>> inv.count
    56

The individual objects contained in the inventory are represented by instances
of the :class:`~sphobjinv.data.DataObjStr` class, which are stored in
a |list| in the :attr:`~sphobjinv.inventory.Inventory.objects` attribute:

.. doctest:: api_inspect

    >>> len(inv.objects)
    56
    >>> dobj = inv.objects[0]
    >>> dobj
    DataObjStr(name='attr.Attribute', domain='py', role='class', priority='1', uri='api.html#$', dispname='-')
    >>> dobj.name
    'attr.Attribute'
    >>> dobj.domain
    'py'

.. warning::

    The contents of this page below this notice are outdated.
    Do not rely on this for working with
    |soi| v2.0

The primary |soi| API consists of two pairs of functions:

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


