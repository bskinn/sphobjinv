.. Instructions for creating and using a custom objects.inv file


Creating and Using a Custom objects.inv
=======================================

.. warning::

    This page is outdated. While the method remains sound
    for ``sphobjinv`` v2.0, the new features added make
    a different workflow preferable in Step 2.

|br|

 1. Identify the head of the URI to the documentation. |br| |br|

 2. Construct an |Inventory| containing all of the objects of interest.
    The :attr:`~sphobjinv.data.SuperDataObj.uri` and
    :attr:`~sphobjinv.data.SuperDataObj.dispname` values
    can be entered with or without the
    :ref:`standard abbreviations <syntax_shorthand>`.

   * Create a blank |Inventory|:

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
         |cour|\ role=method\ |/cour|, not |cour|\ role=meth\ |/cour|.



 3. Export the |Inventory| in compressed form.

   * ...

   * OLD Create the header per the required :doc:`syntax <syntax>`,
     entering the project name and version as appropriate. |br| |br|

   * OLD Create lines of object data, again per the required
     :doc:`syntax <syntax>`.

      * Be sure only to use the relative portion
        of the URI for the ``{uri}`` field.

      * Choose an appropriate domain/role for each object. If necessary
        to avoid conflicts, a `custom domain
        <http://samprocter.com/2014/06/documenting-a-language-using-a-
        custom-sphinx-domain-and-pygments-lexer/>`__ can be created;
        otherwise, one of the `built-in domains
        <http://www.sphinx-doc.org/en/stable/domains.html>`__ may suffice.

 4. Compress the file with |cour|\ sphobjinv convert zlib ...\ |/cour|. |br| |br|

 5. Transfer the compressed file to its distribution location.

   * If only local access is needed, it can be kept local.

   * If external access needed, upload to a suitable host.

 6. Add an element to the |isphxmap|_ parameter in ``conf.py``.

   * The key of the element is an arbitrary name.

   * The value of the element is a |tuple| of length two:

     * The first element of the value tuple is the head URI for the
       documentation repository, to which the
       :meth:`uri <sphobjinv.data.SuperDataObj.uri>` of given object
       is appended when constructing an |isphx| cross-reference.

     * The second element of the value tuple is the complete URL of the
       distribution location of the encoded inventory file,
       whether local or remote.
