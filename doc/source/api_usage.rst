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
    >>> [d.name for d in inv.objects if 'validator' in d.uri]
    ['api_validators', 'examples_validators']


Modifying an Inventory
----------------------

The :class:`~sphobjinv.data.DataObjStr` instances can be edited in place:

.. doctest:: api_modify

    >>> inv = soi.Inventory('objects_attrs.inv')
    >>> inv.objects[0]
    DataObjStr(name='attr.Attribute', domain='py', role='class', priority='1', uri='api.html#$', dispname='-')
    >>> inv.objects[0].uri = 'attribute.html'
    >>> inv.objects[0]
    DataObjStr(name='attr.Attribute', domain='py', role='class', priority='1', uri='attribute.html', dispname='-')

New instances can be easily created either by direct instantiation, or by
:meth:`~sphobjinv.data.DataObjStr.evolve`:

.. doctest:: api_modify

    >>> inv.objects.append(inv.objects[0].evolve(name='attr.Generator', uri='generator.html'))
    >>> inv.count
    57
    >>> inv.objects[-1]
    DataObjStr(name='attr.Generator', domain='py', role='class', priority='1', uri='generator.html', dispname='-')

The other attributes of the :class:`~sphobjinv.inventory.Inventory` instance can also be freely modified:

.. doctest:: api_modify

    >>> inv.project = 'not_attrs'
    >>> inv.version = '0.1'
    >>> print(inv)
    <Inventory (fname_zlib): not_attrs v0.1, 57 objects>


Formatting an Inventory
-----------------------

The contents of the :class:`~sphobjinv.inventory.Inventory` can be converted to
the plaintext |objects.inv| format **as** |bytes| via :meth:`~sphobjinv.inventory.Inventory.data_file`:

.. doctest:: api_formatting

    >>> inv = soi.Inventory('objects_attrs.inv')
    >>> print(*inv.data_file().splitlines()[:6], sep='\n')
    b'# Sphinx inventory version 2'
    b'# Project: attrs'
    b'# Version: 17.2'
    b'# The remainder of this file is compressed using zlib.'
    b'attr.Attribute py:class 1 api.html#$ -'
    b'attr.Factory py:class 1 api.html#$ -'

This method makes use of the :meth:`DataObjStr.data_line <sphobjinv.data.SuperDataObj.data_line>`
method to format each of the object information lines.

If desired, the :ref:`shorthand <syntax_shorthand>` used for the
:attr:`~sphobjinv.data.SuperDataObj.uri` and
:attr:`~sphobjinv.data.SuperDataObj.dispname` fields can be expanded:

.. doctest:: api_formatting

    >>> print(*inv.data_file(expand=True).splitlines()[4:6], sep='\n')
    b'attr.Attribute py:class 1 api.html#attr.Attribute attr.Attribute'
    b'attr.Factory py:class 1 api.html#attr.Factory attr.Factory'
    >>> do = inv.objects[0]
    >>> do.data_line(expand=True)
    'attr.Attribute py:class 1 api.html#attr.Attribute attr.Attribute'

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


