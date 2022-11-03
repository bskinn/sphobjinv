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
    <Inventory (fname_zlib): attrs v22.1, 129 objects>
    >>> inv.version
    '22.1'
    >>> inv.count
    129

The location of the inventory file to import can also be provided as
a :class:`pathlib.Path`, instead of as a string:

.. doctest:: api_inspect

    >>> soi.Inventory(Path('objects_attrs.inv')).project
    'attrs'

The individual objects contained in the inventory are represented by instances
of the :class:`~sphobjinv.data.DataObjStr` class, which are stored in
a |list| in the :attr:`~sphobjinv.inventory.Inventory.objects` attribute:

.. doctest:: api_inspect

    >>> len(inv.objects)
    129
    >>> dobj = inv.objects[0]
    >>> dobj
    DataObjStr(name='attr', domain='py', role='module', priority='0', uri='index.html#module-$', dispname='-')
    >>> dobj.name
    'attr'
    >>> dobj.domain
    'py'
    >>> [d.name for d in inv.objects if 'validator' in d.uri]
    ['api_validators', 'examples_validators']

:class:`~sphobjinv.inventory.Inventory` objects can also import from plaintext or zlib-compressed
inventories, as |bytes|:

.. doctest:: api_inspect

    >>> inv2 = soi.Inventory(inv.data_file())
    >>> print(inv2)
    <Inventory (bytes_plain): attrs v22.1, 129 objects>
    >>> inv3 = soi.Inventory(soi.compress(inv.data_file()))
    >>> print(inv3)
    <Inventory (bytes_zlib): attrs v22.1, 129 objects>

Remote |objects.inv| files can also be retrieved via URL, with the *url* keyword argument:

.. doctest:: api_inspect

    >>> inv4 = soi.Inventory(url='https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv')
    >>> print(inv4)
    <Inventory (url): attrs v22.1, 129 objects>

Comparing Inventories
---------------------

|Inventory| instances compare equal when they have the same :attr:`~sphobjinv.inventory.Inventory.project` and
:attr:`~sphobjinv.inventory.Inventory.version`, and when all the members of
:attr:`~sphobjinv.inventory.Inventory.objects` are identical between the two instances:

.. doctest:: api_compare

    >>> inv = soi.Inventory("objects_attrs.inv")
    >>> inv2 = soi.Inventory(inv.data_file())
    >>> inv is inv2
    False
    >>> inv == inv2
    True
    >>> inv2.project = "foo"
    >>> inv == inv2
    False

Individual |DataObjStr| and (|DataObjBytes|) instances compare equal if all of
:attr:`~sphobjinv.data.SuperDataObj.name`, :attr:`~sphobjinv.data.SuperDataObj.domain`,
:attr:`~sphobjinv.data.SuperDataObj.role`, :attr:`~sphobjinv.data.SuperDataObj.priority`,
:attr:`~sphobjinv.data.SuperDataObj.uri`, and :attr:`~sphobjinv.data.SuperDataObj.dispname`
are equal:

.. doctest:: api_compare

    >>> obj1 = inv.objects[0]
    >>> obj2 = inv.objects[1]
    >>> obj1 == obj1
    True
    >>> obj1 == obj2
    False
    >>> obj1 == obj1.evolve(name="foo")
    False

.. versionchanged:: 2.1
    Previously, |Inventory| instances would only compare equal to themselves,
    and comparison attempts on |SuperDataObj| subclass instances would raise :exc:`RecursionError`.

Modifying an Inventory
----------------------

The :class:`~sphobjinv.data.DataObjStr` instances can be edited in place:

.. doctest:: api_modify

    >>> inv = soi.Inventory('objects_attrs.inv')
    >>> inv.objects[0]
    DataObjStr(name='attr', domain='py', role='module', priority='0', uri='index.html#module-$', dispname='-')
    >>> inv.objects[0].uri = 'attribute.html'
    >>> inv.objects[0]
    DataObjStr(name='attr', domain='py', role='module', priority='0', uri='attribute.html', dispname='-')

New instances can be easily created either by direct instantiation, or by
:meth:`~sphobjinv.data.SuperDataObj.evolve`:

.. doctest:: api_modify

    >>> inv.objects.append(inv.objects[0].evolve(name='attr.Generator', uri='generator.html'))
    >>> inv.count
    130
    >>> inv.objects[-1]
    DataObjStr(name='attr.Generator', domain='py', role='module', priority='0', uri='generator.html', dispname='-')

The other attributes of the :class:`~sphobjinv.inventory.Inventory` instance can also be freely modified:

.. doctest:: api_modify

    >>> inv.project = 'not_attrs'
    >>> inv.version = '0.1'
    >>> print(inv)
    <Inventory (fname_zlib): not_attrs v0.1, 130 objects>


Formatting Inventory Contents
-----------------------------

The contents of the :class:`~sphobjinv.inventory.Inventory` can be converted to
the plaintext |objects.inv| format **as** |bytes| via :meth:`~sphobjinv.inventory.Inventory.data_file`:

.. doctest:: api_formatting

    >>> inv = soi.Inventory('objects_attrs.inv')
    >>> print(*inv.data_file().splitlines()[:6], sep='\n')
    b'# Sphinx inventory version 2'
    b'# Project: attrs'
    b'# Version: 22.1'
    b'# The remainder of this file is compressed using zlib.'
    b'attr py:module 0 index.html#module-$ -'
    b'attr.VersionInfo py:class 1 api.html#$ -'

This method makes use of the :meth:`DataObjStr.data_line <sphobjinv.data.SuperDataObj.data_line>`
method to format each of the object information lines.

If desired, the :ref:`shorthand <syntax_shorthand>` used for the
:attr:`~sphobjinv.data.SuperDataObj.uri` and
:attr:`~sphobjinv.data.SuperDataObj.dispname` fields can be expanded:

.. doctest:: api_formatting

    >>> print(*inv.data_file(expand=True).splitlines()[4:6], sep='\n')
    b'attr py:module 0 index.html#module-attr attr'
    b'attr.VersionInfo py:class 1 api.html#attr.VersionInfo attr.VersionInfo'
    >>> do = inv.objects[0]
    >>> do.data_line(expand=True)
    'attr py:module 0 index.html#module-attr attr'


Exporting an Inventory
----------------------

:class:`~sphobjinv.inventory.Inventory` instances can be written to disk
in three formats: zlib-compressed |objects.inv|,
plaintext |objects.txt|, and JSON. The API does not provide single-function
means to do this, however.

To start, load the source |objects.inv|:

.. doctest:: api_exporting

    >>> from pathlib import Path
    >>> inv = soi.Inventory('objects_attrs.inv')

To export plaintext:

.. doctest:: api_exporting

    >>> df = inv.data_file()
    >>> soi.writebytes('objects_attrs.txt', df)
    >>> print(*Path('objects_attrs.txt').read_text().splitlines()[:6], sep='\n')
    # Sphinx inventory version 2
    # Project: attrs
    # Version: 22.1
    # The remainder of this file is compressed using zlib.
    attr py:module 0 index.html#module-$ -
    attr.VersionInfo py:class 1 api.html#$ -

For zlib-compressed:

.. doctest:: api_exporting

    >>> dfc = soi.compress(df)
    >>> soi.writebytes('objects_attrs_new.inv', dfc)
    >>> print(*Path('objects_attrs_new.inv').read_bytes().splitlines()[:4], sep='\n')
    b'# Sphinx inventory version 2'
    b'# Project: attrs'
    b'# Version: 22.1'
    b'# The remainder of this file is compressed using zlib.'
    >>> print(Path('objects_attrs_new.inv').read_bytes().splitlines()[6][:10])
    b'\xbf\x86\x8fL49\xc4\x91\xb8\x8c'

For JSON:

.. doctest:: api_exporting

    >>> jd = inv.json_dict()
    >>> soi.writejson('objects_attrs.json', jd)
    >>> print(Path('objects_attrs.json').read_text()[:51])  # doctest: +SKIP
    {"project": "attrs", "version": "17.2", "count": 56
