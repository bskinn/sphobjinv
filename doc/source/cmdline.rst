.. Description of commandline usage

Command-Line Usage
==================

.. warning::

    This page is outdated. Do not rely on it for working with
    |soi| v2.0

The CLI for |soi| is implemented using two subparsers, one each for the
convert and suggest sub-functions. *(Add option links once pages in place.)*


In the CLI execution examples below and in the pages describing the subparser
options, file paths in CLI output are elided (with |cour|\ ...\ |/cour|)
so that doctests will pass in all of my various development environments.
The motivation for using |cour|\ cli_run\ |/cour| is described in more
detail `here <https://bskinn.github.io/Testing-CLI-Scripts/>`__.
In all cases, examples are executed in a sandboxed directory pre-loaded with
|cour|\ objects_attrs.inv\ |/cour| (from, e.g.,
`here <https://github.com/bskinn/sphobjinv/blob/master/sphobjinv/test/resource/objects_attrs.inv>`__).




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
    sphobjinv v2.0rc1
    <BLANKLINE>
    Copyright (c) Brian Skinn 2016-2018
    License: The MIT License
    <BLANKLINE>
    Bug reports & feature requests: https://github.com/bskinn/sphobjinv
    Documentation: http://sphobjinv.readthedocs.io
    <BLANKLINE>
    <BLANKLINE>




.. toctree::
    :maxdepth: 1
    :hidden:

    "convert" Mode <cli/convert>
    "suggest" Mode <cli/suggest>



Old content
-----------

On most systems, |soi| should automatically install with a command
line / shell script inserted into {python}/Scripts and thus be executable
from anywhere.

Argument handling for both encode and decode operations has been written in an
attempt to make using the script as user-friendly as possible.  The script has
the following usage syntax (Windows version shown):

.. code-block:: none

    > sphobjinv --help

    usage: sphobjinv-script.py [-h] {encode,decode} [infile] [outfile]

    Decode/encode intersphinx 'objects.inv' files.

    positional arguments:
      {encode,decode}  Conversion mode
      infile           Path to file to be decoded (encoded). Defaults to
                       './objects.inv(.txt)'. Bare paths are accepted, in which
                       case the above default input file names are used in the
                       indicated path. '-' is a synonym for these defaults.
      outfile          Path to decoded (encoded) output file. Defaults to same
                       directory and main file name as input file but with
                       extension .txt (.inv). Bare paths are accepted here as
                       well, using the default output file names.

    optional arguments:
      -h, --help       show this help message and exit

In particular, note the default input file names (|objects.inv| and
|objects.txt|), and the ability to select these default file names in
a given directory by simply passing the path to that directory.


**Examples**

All of the below are decode operations executed on Windows; encode operations
behave essentially the same, except for swapping the default input/output
file extensions. Adapt the path syntax, etc. as appropriate for the relevant
operating system.

To decode a file with the Sphinx-default name of |objects.inv| residing in the
current directory, to the default output file of |objects.txt|:

.. code-block:: none

    > sphobjinv decode

    Conversion completed.
    '.\objects.inv' decoded to '.\objects.txt'.

To decode the same |objects.inv| file to |cour|\ objects_custom.\ |/cour|:

.. code-block:: none

    > sphobjinv decode - objects_custom.

    Conversion completed.
    '.\objects.inv' decoded to '.\objects_custom.'.

To decode |cour|\ objects_python.inv\ |/cour| residing in the root directory to
|cour|\ objects_python.txt\ |/cour| in the directory |cour|\ \\temp\ |/cour|:

.. code-block:: none

    > sphobjinv decode \objects_python.inv \temp

    Conversion completed.
    '\objects_python.inv' decoded to '\temp\objects_python.txt'.

To decode the same |cour|\ objects_python.inv\ |/cour| to
|cour|\ new_objects.txt\ |/cour| in the directory
|cour|\ \\git\ |/cour|:

.. code-block:: none

    > sphobjinv decode \objects_python.inv \git\new_objects.txt

    Conversion completed.
    '\objects_python.inv' decoded to '\git\new_objects.txt'.

