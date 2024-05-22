.. Instructions for creating and using a custom objects.inv file


Creating and Using a Custom objects.inv
=======================================

The workflow presented here is introduced in the context of manually
assembling an objects inventory, but the functionality is mainly
intended for use downstream of a web-scraping or other automated
content-extraction tool.

A (possibly obsolete) representative example of such a custom |objects.inv|
can be found at the GitHub repo
`here <https://github.com/bskinn/intersphinx-xlwsf>`__.

.. note::

    These instructions are for |soi| v2.x;
    the prior instructions for v1.0 can be found
    `here <https://sphobjinv.readthedocs.io/en/v1.0.post1/customfile.html>`__.

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
            <Inventory (manual): <no project> <no version>, 0 objects>

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

            The `role` values here must be the **full** role names ("`block directives`"),
            described as the "directives" in the `Sphinx documentation for
            domains <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-python-domain>`__,
            and not the abbreviated forms ("`inline directives`")
            `used when constructing cross-references
            <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-python-objects>`__.

            Thus, for example, a :class:`~sphobjinv.data.DataObjStr` corresponding
            to a method on a class should be constructed with
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

    * If external access needed, upload to a suitable host. |br|

#. Add an element to the |isphxmap|_ parameter in ``conf.py``.

    * The key of the element is an arbitrary name, which can be used
      to specify the desired documentation set to be searched
      for the target object, in the event of a `name` collision
      between one or more documentation projects; e.g.::

          :meth:`python:str.join`

    * The value of the element is a |tuple| of length two:

        * The first element of the value tuple is the head URI for the
          documentation repository,
          identified in step (1),
          to which the
          :attr:`~sphobjinv.data.SuperDataObj.uri` of given object
          is appended when constructing an |isphx| cross-reference.

        * The second element of the value tuple can be |None|, in which case
          the |objects.inv| file is assumed to be at the repository head URI.
          Otherwise, this element is the complete address of the
          distribution location of the compressed inventory file,
          from step (4), whether a local path or a remote URL.

    Examples:

        .. code::

            intersphinx_mapping = {
                # Standard reference to web docs, with web objects.inv
                'python': ('https://docs.python.org/3.12', None),

                # Django puts its objects.inv file in a non-standard location
                'django': ('https://docs.djangoproject.com/en/dev/', 'https://docs.djangoproject.com/en/dev/_objects/'),

                # Drawing the Sphinx objects.inv from a local copy, but referring to the current web docs
                'sphinx': ('https://www.sphinx-doc.org/en/master/', '/path/to/local/objects.inv'),
            }

    .. MAKE SURE TO UPDATE THESE TWO STEP REFERENCES IF NUMBERING CHANGES!!
