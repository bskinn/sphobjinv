.. Description of commandline usage

Command-Line Usage
==================

The CLI for |soi| is implemented using two subparsers, one each for the
:doc:`convert <convert>` and :doc:`suggest <suggest>` sub-functions.
More information about the implementation of these features can be
found :doc:`here <implementation>` and in the documentation for the
:class:`~sphobjinv.inventory.Inventory` object, in particular the
:meth:`~sphobjinv.inventory.Inventory.data_file` and
:meth:`~sphobjinv.inventory.Inventory.suggest` methods.

Some notes on these CLI docs:

 * CLI examples are executed in a sandboxed directory pre-loaded with
   |cour|\ objects_attrs.inv\ |/cour| (from, e.g.,
   `here <https://github.com/bskinn/sphobjinv/blob/master/sphobjinv/
   test/resource/objects_attrs.inv>`__).

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

.. doctest:: soi_base

    >>> cli_run('sphobjinv --help')
    usage: sphobjinv [-h] [-v] {convert,suggest} ...
    <BLANKLINE>
    Format conversion for and introspection of intersphinx 'objects.inv' files.
    <BLANKLINE>
    optional arguments:
      -h, --help         show this help message and exit
      -v, --version      Print package version & other info
    <BLANKLINE>
    Subcommands:
      {convert,suggest}  Execution mode. Type 'sphobjinv [mode] -h' for more
                         information on available options. Mode names can be
                         abbreviated to their first two letters.
        convert (co)     Convert intersphinx inventory to zlib-compressed,
                         plaintext, or JSON formats.
        suggest (su)     Fuzzy-search intersphinx inventory for desired object(s).
    <BLANKLINE>


.. option:: -v, --version

    Print package version & other info

.. doctest:: soi_base

    >>> cli_run('sphobjinv --version')
    <BLANKLINE>
    sphobjinv v2.0.1rc1
    <BLANKLINE>
    Copyright (c) Brian Skinn 2016-2019
    License: The MIT License
    <BLANKLINE>
    Bug reports & feature requests: https://github.com/bskinn/sphobjinv
    Documentation: http://sphobjinv.readthedocs.io
    <BLANKLINE>
    <BLANKLINE>




.. toctree::
    :maxdepth: 1
    :hidden:

    "convert" Mode <convert>
    "suggest" Mode <suggest>


