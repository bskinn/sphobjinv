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
``sphobjinv-textconv`` (:doc:`docs page <textconv>`), which takes a path
to a file on disk as its single required argument. This entrypoint attempts
to instantiate an |Inventory| with this file and emit its plaintext
contents to |stdout|. The following two invocations are thus synonymous::

    $ sphobjinv convert plain path/to/objects.inv -

    $ sphobjinv-textconv path/to/objects.inv

This alternative spelling is less awkward when configuring a Git ``textconv`` to
allow rendering diffs of |objects.inv| files in plaintext. See the
``sphobjinv-textconv`` :doc:`entrypoint documentation <textconv>` for more
information.

----

Some notes on these CLI docs:

 * CLI docs examples are executed in a sandboxed directory pre-loaded with
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
