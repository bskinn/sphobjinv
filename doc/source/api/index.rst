.. API page

API
===

Most (all?) of the objects documented in the below submodules
are also exposed at the |soi| package root. For example,
both of the following will work to import the
:class:`~sphobjinv.inventory.Inventory` class:

.. doctest:: api_index

    >>> from sphobjinv import Inventory
    >>> from sphobjinv.inventory import Inventory


.. toctree::
    :maxdepth: 1

    data
    enum
    error
    fileops
    inventory
    re
    schema
    zlib
