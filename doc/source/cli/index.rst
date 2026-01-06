.. Description of commandline usage

Command-Line Usage
==================

The primary CLI for |soi| is implemented using two subcommands of the
``sphobjinv`` entrypoint:

  - ``sphobjinv convert`` (:doc:`docs page <convert>`), which handles conversion
    of inventories between supported formats (currently zlib-compressed,
    plaintext, and JSON).
  - ``sphobjinv suggest`` (:doc:`docs page <suggest>`), which provides suggestions for
    objects in an inventory matching a desired search term.

As of v##VER##, |soi| also provides an auxiliary entrypoint,
``sphobjinv-textconv`` (:doc:`docs page <textconv>`), which takes one required
argument: a path to a file on disk. This entrypoint attempts to instantiate an
|Inventory| with this file and emit its plaintext contents to |stdout| with no
cosmetic whitespace. The following two invocations are thus nearly synonymous::

    $ sphobjinv convert plain path/to/objects.inv -

    $ sphobjinv-textconv path/to/objects.inv

(Be sure to note the final hyphen in the first command.) The
``sphobjinv-textconv`` spelling is less awkward when configuring a Git
|textconv| to allow rendering diffs of |objects.inv| files in plaintext. See the
``sphobjinv-textconv`` :doc:`entrypoint documentation <textconv>` for more
information.

----

Shell examples in the CLI docs execute from within |cour|\ /tests/resource\
|/cour| unless indicated otherwise.

For Python examples:

 * Examples are executed in a sandboxed directory pre-loaded with
   |cour|\ objects_attrs.inv\ |/cour| (from, e.g.,
   `here <https://github.com/bskinn/sphobjinv/blob/main/
   tests/resource/objects_attrs.inv>`__).

 * :class:`~pathlib.Path` (from :mod:`pathlib`)
   is imported into the namespace before all tests.

 * |cour|\ cli_run\ |/cour| is a helper function that enables doctesting
   of CLI examples by mimicking execution of a shell command.
   It is described in more detail
   `here <https://bskinn.github.io/Testing-CLI-Scripts/>`__.

 * |cour|\ file_head\ |/cour| is a helper function
   that retrieves the head of a specified file.

.. toctree::
    :maxdepth: 1
    :hidden:

    sphobjinv convert <convert>
    sphobjinv suggest <suggest>
    sphobjinv-textconv <textconv>
