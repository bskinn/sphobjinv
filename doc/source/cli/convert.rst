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

Basic file conversion is straightforward:

.. doctest:: convert

    >>> from pathlib import Path
    >>> Path('objects_attrs.txt').is_file()
    False
    >>> cli_run('sphobjinv convert plain objects_attrs.inv')
    <BLANKLINE>
    Conversion completed.
    '...objects_attrs.inv' converted to '...objects_attrs.txt' (plain).
    <BLANKLINE>
    >>> print('\n'.join(Path('objects_attrs.txt').read_text().splitlines()[:6]))
    # Sphinx inventory version 2
    # Project: attrs
    # Version: 17.2
    # The remainder of this file is compressed using zlib.
    attr.Attribute py:class 1 api.html#$ -
    attr.Factory py:class 1 api.html#$ -


**Usage**

.. doctest:: convert_usage

    >>> cli_run('sphobjinv convert --help', head=4)
    usage: sphobjinv convert [-h] [-e | -c] [-o] [-q] [-u]
                             {zlib,plain,json} infile [outfile]
    <BLANKLINE>
    Convert intersphinx inventory to zlib-compressed, plaintext, or JSON formats.

**Required Arguments**

.. option:: mode

    Conversion output format.

    Must be one of `plain`, `zlib`, or `json`

.. option:: infile

    Path (or URL, if :option:`--url` is specified) to file to be converted.

.. option:: outfile

    Path to desired output file. Defaults to same directory
    and main file name as input file but with extension
    |cour|\ .inv/.txt/.json\ |/cour|, as appropriate for the output format.
    A bare path is accepted here, using the default output
    file name/extension.

**Optional Arguments**

.. option:: -h, --help

    Display `convert` help message and exit