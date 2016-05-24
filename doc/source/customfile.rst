.. Instructions for creating and using a custom objects.inv file


Creating and Using a Custom objects.inv
=======================================

 1. Identify the head of the URI to the documentation. |br| |br|

 2. Create the custom ``objects.inv`` file.

   * Create the header per the required :doc:`syntax <syntax>`,
     entering the project name and version as appropriate. |br| |br|

   * Create lines of object data, again per the required
     :doc:`syntax <syntax>`.

      * Be sure only to use the relative portion
        of the URI for the ``{uri}`` field.

      * Choose an appropriate domain/role for each object. If necessary
        to avoid conflicts, a `custom domain
        <http://samprocter.com/2014/06/documenting-a-language-using-a-
        custom-sphinx-domain-and-pygments-lexer/>`__ can be created;
        otherwise, one of the `built-in domains
        <http://www.sphinx-doc.org/en/stable/domains.html>`__ may suffice.

 3. Encode the file with ``sphobjinv``. |br| |br|

 4. Transfer the encoded file to its distribution location.

   * If only local access is needed, it can be kept local.

   * If external access needed, upload to a suitable host.

 5. Add an element to the ``intersphinx_mapping`` parameter in ``conf.py``.

   * The element key is arbitrary.

   * The first element of the value tuple is the head URI for the
     repository.

   * The second element of the value tuple is the address of the
     distribution location of the encoded file.
