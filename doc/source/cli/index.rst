.. Description of commandline usage

Command-Line Usage
==================

The CLI for |soi| is implemented using two subcommands:

  - A :doc:`convert <convert>` subcommand, which handles conversion of
    inventories between supported formats (currently zlib-compressed,
    plaintext, and JSON).
  - A :doc:`suggest <suggest>` subcommand, which provides suggestions for
    objects in an inventory matching a desired search term.

More information about the underlying implementation of these subcommands can
be found :doc:`here <implementation/index>` and in the documentation for the
:class:`~sphobjinv.inventory.Inventory` object, in particular the
:meth:`~sphobjinv.inventory.Inventory.data_file` and
:meth:`~sphobjinv.inventory.Inventory.suggest` methods.

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


.. program:: sphobjinv

The options for the parent |soi| command are:

.. option:: -h, --help

    Show help message and exit

.. program-output:: sphobjinv --help


.. option:: -v, --version

    Print package version & other info

.. program-output:: sphobjinv --version


.. toctree::
    :maxdepth: 1
    :hidden:

    "convert" Mode <convert>
    "suggest" Mode <suggest>
