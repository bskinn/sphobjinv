.. Description of commandline usage

Command-Line Usage
==================

.. warning::

    This page is outdated. Do not rely on it for working with
    ``sphobjinv`` v2.0

**Mention ellipses on filenames, provenance of** `cli_run`
**(probably would be good to add link to GH showing implementation,
for any who might be curious), pre-loading of** `objects_attrs.inv`
**to scratch directory, ....**

**ALSO: Probably going to want to split this into** `suggest` **and**
`convert` **subpages... there's enough there to warrant the split,
especially with it being handled by subparsers. The help views themselves
are going to be enormous....**

.. doctest:: scratch

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
    >>> cli_run('sphobjinv convert plain objects_attrs.inv')
    <BLANKLINE>
    Conversion completed.
    '.../objects_attrs.inv' converted to '.../objects_attrs.txt' (plain).
    <BLANKLINE>
    >>> cli_run('sphobjinv convert plain objects_attrs.inv', inp='y\n')
    File exists. Overwrite (Y/N)? y
    <BLANKLINE>
    Conversion completed.
    '.../objects_attrs.inv' converted to '.../objects_attrs.txt' (plain).
    <BLANKLINE>


Old content
-----------

On most systems, ``sphobjinv`` should automatically install with a command
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

In particular, note the default input file names (``objects.inv`` and
``objects.txt``), and the ability to select these default file names in
a given directory by simply passing the path to that directory.


**Examples**

All of the below are decode operations executed on Windows; encode operations
behave essentially the same, except for swapping the default input/output
file extensions. Adapt the path syntax, etc. as appropriate for the relevant
operating system.

To decode a file with the Sphinx-default name of ``objects.inv`` residing in the
current directory, to the default output file of ``objects.txt``:

.. code-block:: none

    > sphobjinv decode

    Conversion completed.
    '.\objects.inv' decoded to '.\objects.txt'.

To decode the same ``objects.inv`` file to ``objects_custom.``:

.. code-block:: none

    > sphobjinv decode - objects_custom.

    Conversion completed.
    '.\objects.inv' decoded to '.\objects_custom.'.

To decode ``objects_python.inv`` residing in the root directory to
``objects_python.txt`` in the directory ``\temp``:

.. code-block:: none

    > sphobjinv decode \objects_python.inv \temp

    Conversion completed.
    '\objects_python.inv' decoded to '\temp\objects_python.txt'.

To decode the same ``objects_python.inv`` to ``new_objects.txt``
in the directory ``\git``:

.. code-block:: none

    > sphobjinv decode \objects_python.inv \git\new_objects.txt

    Conversion completed.
    '\objects_python.inv' decoded to '\git\new_objects.txt'.

