.. Description of sphobjinv-textconv commandline usage

Command-Line Usage: ``sphobjinv-textconv``
==========================================

.. program:: sphobjinv-textconv

``sphobjinv-textconv`` is intentionally implemented with very narrow functionality,
specifically to simplify configuring |soi| for use as a
`Git "textconv" <https://git-scm.com/docs/gitattributes#_performing_text_diffs_of_binary_files>`__,
which is a mechanism for rendering binary files in a diff-able text format. There are
many examples of `clever`_ application of textconv in the wild.

Ultimately, a textconv involves three things:

1. A utility that takes in a file path as a single positional argument.

2. An entry somewhere in Git config declaring a 


----

Basic file conversion to the default output filename is straightforward:

.. doctest:: convert_main

    >>> Path('objects_attrs.txt').is_file()
    False
    >>> cli_run('sphobjinv convert plain objects_attrs.inv')
    <BLANKLINE>
    Conversion completed.
    '...objects_attrs.inv' converted to '...objects_attrs.txt' (plain).
    <BLANKLINE>
    <BLANKLINE>
    >>> print(file_head('objects_attrs.txt', head=6))
    # Sphinx inventory version 2
    # Project: attrs
    # Version: 22.1
    # The remainder of this file is compressed using zlib.
    attr py:module 0 index.html#module-$ -
    attr.VersionInfo py:class 1 api.html#$ -

A different target filename can be specified, to avoid overwriting an existing
file:




**Usage**

.. command-output:: sphobjinv-textconv --help
    :ellipsis: 4


**Positional Arguments**

.. option:: infile

    Path to file to be emitted to |stdout| in plaintext.

**Flags**

.. option:: -h, --help

    Display help message and exit.

.. option:: -v, --version

    Display brief package version information and exit.

.. versionadded:: ##VER##

.. _clever: https://github.com/syntevosmartgit/textconv
