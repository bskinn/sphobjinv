.. Description of convert commandline usage

Command-Line Usage: "convert" Mode
==================================

.. program:: sphobjinv convert

The |cour|\ convert\ |/cour| subparser is used for all conversions of inventory
files among plaintext, zlib-compressed, and (unique to |soi|) JSON formats.
Currently, the |soi| CLI can read |objects.inv| files from local files
in any of these three formats, as well as standard zlib-compressed files
from remote locations (see :option:`--url`). At the moment, the only output
method supported is writing to a local file, again in all three formats.

.. note::

    If reading from |stdin| or writing to |stdout| would be useful to you,
    please leave a note at :issue:`74` so I can gauge interest.

Basic file conversion to the default output filename is straightforward:

.. doctest:: convert_main

    >>> Path('objects_attrs.txt').is_file()
    False
    >>> cli_run('sphobjinv convert plain objects_attrs.inv')
    <BLANKLINE>
    Conversion completed.
    '...objects_attrs.inv' converted to '...objects_attrs.txt' (plain).
    <BLANKLINE>
    >>> print(file_head('objects_attrs.txt', head=6))
    # Sphinx inventory version 2
    # Project: attrs
    # Version: 17.2
    # The remainder of this file is compressed using zlib.
    attr.Attribute py:class 1 api.html#$ -
    attr.Factory py:class 1 api.html#$ -

A different target filename can be specified, to avoid overwriting an existing
file:

.. doctest:: convert_main

    >>> cli_run('sphobjinv convert plain objects_attrs.inv', inp='n\n')
    File exists. Overwrite (Y/N)? n
    <BLANKLINE>
    Exiting...
    <BLANKLINE>
    >>> cli_run('sphobjinv convert plain objects_attrs.inv objects_attrs_foo.txt')
    <BLANKLINE>
    Conversion completed.
    '...objects_attrs.inv' converted to '...objects_attrs_foo.txt' (plain).
    <BLANKLINE>

If you don't provide an output file extension, the |soi| defaults
(`.inv`/`.txt`/`.json`) will be used.

If you want to pull an input file directly from the Web, use
:option:`--url` (note that the base filename is **not** inferred from the
indicated URL):

.. doctest:: convert_url

    >>> cli_run('sphobjinv convert plain -u https://github.com/bskinn/sphobjinv/raw/dev/sphobjinv/test/resource/objects_attrs.inv')
    <BLANKLINE>
    Conversion completed.
    'https://github.com/b[...]ce/objects_attrs.inv' converted to '...objects.txt' (plain).
    <BLANKLINE>
    >>> print(file_head('objects.txt', head=6))
    # Sphinx inventory version 2
    # Project: attrs
    # Version: 17.2
    # The remainder of this file is compressed using zlib.
    attr.Attribute py:class 1 api.html#$ -
    attr.Factory py:class 1 api.html#$ -

Note that |soi| only supports download of zlib-compressed |objects.inv| files by URL.
Plaintext download by URL is unreliable, presumably due to encoding problems.
If download of JSON files by URL is desirable, please
`submit an issue <https://github.com/bskinn/sphobjinv/issues>`__.

**Usage**

.. doctest:: convert_usage

    >>> cli_run('sphobjinv convert --help', head=4)
    usage: sphobjinv convert [-h] [-e | -c] [-o] [-q] [-u]
                             {zlib,plain,json} infile [outfile]
    <BLANKLINE>
    Convert intersphinx inventory to zlib-compressed, plaintext, or JSON formats.

**Positional Arguments**

.. option:: mode

    Conversion output format.

    Must be one of `plain`, `zlib`, or `json`

.. option:: infile

    Path (or URL, if :option:`--url` is specified) to file to be converted.

.. option:: outfile

    *(Optional)* Path to desired output file. Defaults to same directory
    and main file name as input file but with extension
    |cour|\ .inv/.txt/.json\ |/cour|, as appropriate for the output format.
    A bare path is accepted here, using the default output
    file name/extension.

**Flags**

.. option:: -h, --help

    Display `convert` help message and exit.

.. option:: -o, --overwrite

    If the output file already exists, overwrite without prompting
    for confirmation.

.. option:: -q, --quiet

    Suppress all output to `stdout`, regardless of success or failure.
    Useful for scripting/automation.  Implies :option:`--overwrite`.

.. option:: -u, --url

    Treat :option:`infile` as a URL for download.

.. option:: -e, --expand

    Expand any abbreviations in `uri` or `dispname` fields before writing to output;
    see :ref:`here <syntax_shorthand>`. Cannot be specified with
    :option:`--contract`.

.. option:: -c, --contract

    Contract `uri` and `dispname` fields, if possible, before writing to output;
    see :ref:`here <syntax_shorthand>`. Cannot be specified with
    :option:`--expand`.

