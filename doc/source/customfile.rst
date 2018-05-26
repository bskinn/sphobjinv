.. Instructions for creating and using a custom objects.inv file


Creating and Using a Custom objects.inv
=======================================

The workflow presented here is introduced in the context of manually
assembling an objects inventory, but the functionality is mainly
intended for use downstream of a web-scraping or other automated
content-extraction tool.

 #. Identify the head of the URI to the documentation. |br| |br|


 #. Construct an |Inventory| containing all of the objects of interest.
    The :attr:`~sphobjinv.data.SuperDataObj.uri` and
    :attr:`~sphobjinv.data.SuperDataObj.dispname` values
    can be entered with or without the
    :ref:`standard abbreviations <syntax_shorthand>`.

    * Create an empty |Inventory|:

        .. doctest:: customfile

            >>> import sphobjinv as soi
            >>> inv = soi.Inventory()
            >>> print(inv)
            <Inventory (manual): None vNone, 0 objects>

    * Define the :attr:`~sphobjinv.inventory.Inventory.project`
      and :attr:`~sphobjinv.inventory.Inventory.version` attributes:

        .. doctest:: customfile

            >>> inv.project = 'foobar'
            >>> inv.version = '1.5'
            >>> print(inv)
            <Inventory (manual): foobar v1.5, 0 objects>

    * Append new :class:`~sphobjinv.data.DataObjStr` instances to
      :attr:`~sphobjinv.inventory.Inventory.objects` as needed
      to populate the inventory:

        .. doctest:: customfile

            >>> o = soi.DataObjStr(name='baz', domain='py', role='class',
            ... priority='1', uri='api.html#$', dispname='-')
            >>> print(o)
            <DataObjStr:: :py:class:`baz`>
            >>> inv.objects.append(o)
            >>> print(inv)
            <Inventory (manual): foobar v1.5, 1 objects>
            >>> inv.objects.append(soi.DataObjStr(name='baz.quux', domain='py',
            ... role='method', priority='1', uri='api.html#$', dispname='-'))
            >>> inv.objects.append(soi.DataObjStr(name='quuux', domain='py',
            ... role='function', priority='1', uri='api.html#$', dispname='-'))
            >>> print(inv)
            <Inventory (manual): foobar v1.5, 3 objects>

        .. note::

            The `role` values here must be the **full** role names,
            described as the "directives" in the `Sphinx documentation for
            domains <http://www.sphinx-doc.org/en/1.7/domains.html#the-python-domain>`__,
            and not the abbreviated forms `used when constructing cross-references
            <http://www.sphinx-doc.org/en/1.7/domains.html#cross-referencing-python-objects>`__.

            Thus, for example, a :class:`~sphobjinv.data.DataObjStr` corresponding
            to a method on a class should be instantiated with
            |cour|\ role='method'\ |/cour|, not |cour|\ role='meth'\ |/cour|.



 #. Export the |Inventory| in compressed form.

    * Generate the text of the inventory file
      with :meth:`~sphobjinv.inventory.Inventory.data_file`,
      optionally :ref:`contracting <syntax_shorthand>` the
      :attr:`~sphobjinv.data.SuperDataObj.uri` and
      :attr:`~sphobjinv.data.SuperDataObj.dispname` fields:

        .. doctest:: customfile

            >>> text = inv.data_file(contract=True)

    * Compress the file text:

        .. doctest:: customfile

            >>> ztext = soi.compress(text)

    * Save to disk:

        .. doctest:: customfile

            >>> soi.writebytes('objects_foobar.inv', ztext)


 #. Transfer the compressed file to its distribution location.

    * If only local access is needed, it can be kept local.

    * If external access needed, upload to a suitable host. |br| |br|

 #. Add an element to the |isphxmap|_ parameter in ``conf.py``.

    * The key of the element is an arbitrary name, which can be used
      to specify the desired documentation set to be searched
      for the target object, in the event of a `name` collision; e.g.::

          :meth:`python:str.join`

    * The value of the element is a |tuple| of length two:

        * The first element of the value tuple is the head URI for the
          documentation repository,
          identified in step (1),
          to which the
          :attr:`~sphobjinv.data.SuperDataObj.uri` of given object
          is appended when constructing an |isphx| cross-reference.

        * The second element of the value tuple is the complete URL of the
          distribution location of the compressed inventory file,
          from step (4), whether local
          (|cour|\ file:\ ///\ |/cour|)
          or remote
          (e.g., |cour|\ http:\ //\ |/cour|)

        .. MAKE SURE TO UPDATE THESE TWO STEP REFERENCES IF NUMBERING CHANGES!!
