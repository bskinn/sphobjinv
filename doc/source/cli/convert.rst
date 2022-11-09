.. Description of convert commandline usage

Command-Line Usage: "convert" Subcommand
========================================

.. program:: sphobjinv convert

The |cour|\ convert\ |/cour| subcommand is used for all conversions of
"version 2" Sphinx inventory
files among plaintext, zlib-compressed, and (unique to |soi|) JSON formats.
The |soi| CLI can read and write inventory data from local files
in any of these three formats, as well as read the standard zlib-compressed format
from files in remote locations (see :option:`--url`).

As of v2.1, the |soi| CLI can also read/write inventories at ``stdin``/``stdout``
in the plaintext and JSON formats; see :ref:`below <cli_usage_json_added>`.

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

.. doctest:: convert_main

    >>> cli_run('sphobjinv convert plain objects_attrs.inv', inp='n\n')
    File exists. Overwrite (Y/N)? n
    <BLANKLINE>
    <BLANKLINE>
    Exiting...
    <BLANKLINE>
    >>> cli_run('sphobjinv convert plain objects_attrs.inv objects_attrs_foo.txt')
    <BLANKLINE>
    Conversion completed.
    '...objects_attrs.inv' converted to '...objects_attrs_foo.txt' (plain).
    <BLANKLINE>
    <BLANKLINE>

If you don't provide an output file extension, the |soi| defaults
(`.inv`/`.txt`/`.json`) will be used.

If you want to pull an input file directly from the internet, use
:option:`--url` (note that the base filename is **not** inferred from the
indicated URL):

.. doctest:: convert_url

    >>> cli_run('sphobjinv convert plain -u https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv')
    <BLANKLINE>
    Attempting https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv ...
      ... inventory found.
    <BLANKLINE>
    Conversion completed.
    'https://github.com/b[...]ce/objects_attrs.inv' converted to '...objects.txt' (plain).
    <BLANKLINE>
    <BLANKLINE>
    >>> print(file_head('objects.txt', head=6))
    # Sphinx inventory version 2
    # Project: attrs
    # Version: 22.1
    # The remainder of this file is compressed using zlib.
    attr py:module 0 index.html#module-$ -
    attr.VersionInfo py:class 1 api.html#$ -

The URL provided **MUST** have the leading protocol specified (here,
|cour|\ https\ ://\ |/cour|).

It is not necessary to locate the |objects.inv| file before running |soi|;
for most Sphinx documentation sets, if you provide a URL to any page in the docs,
it will automatically find and use the correct |objects.inv|:

.. doctest:: convert_url

    >>> cli_run('sphobjinv convert plain -ou https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError')
    <BLANKLINE>
    Attempting https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError ...
      ... no recognized inventory.
    Attempting "https://docs.python.org/3/library/urllib.error.html/objects.inv" ...
      ... HTTP error: 404 Not Found.
    Attempting "https://docs.python.org/3/library/objects.inv" ...
      ... HTTP error: 404 Not Found.
    Attempting "https://docs.python.org/3/objects.inv" ...
      ... inventory found.
    <BLANKLINE>
    Conversion completed.
    '...objects.inv' converted to '...objects.txt' (plain).
    <BLANKLINE>
    <BLANKLINE>

|soi| only supports download of zlib-compressed |objects.inv| files by URL.
Plaintext download by URL is unreliable, presumably due to encoding problems.
If processing of JSON files by API URL is desirable, please
`submit an issue <https://github.com/bskinn/sphobjinv/issues>`__.

.. versionadded:: 2.1
    The URL at which a remote inventory is found is now included
    in JSON output:

    .. doctest:: json-url

        >>> cli_run('sphobjinv convert json -qu https://docs.python.org/3/ objects.json')
        <BLANKLINE>
        >>> data = json.loads(Path('objects.json').read_text())
        >>> data["metadata"]["url"]
        'https://docs.python.org/3/objects.inv'

.. _cli_usage_json_added:

.. versionadded:: 2.1
    JSON and plaintext inventories can now be read from ``stdin`` and
    written to ``stdout``, by using the special value ``-`` in the invocation.
    E.g., to print to ``stdout``:

    .. doctest:: stdio

        >>> cli_run('sphobjinv co plain objects_attrs.inv -')
        # Sphinx inventory version 2
        # Project: attrs
        # Version: 22.1
        # The remainder of this file is compressed using zlib.
        attr py:module 0 index.html#module-$ -
        attr.VersionInfo py:class 1 api.html#$ -
        attr._make.Attribute py:class -1 api.html#attrs.Attribute -
        ...


**Usage**

.. command-output:: sphobjinv convert --help
    :ellipsis: 4


**Positional Arguments**

.. option:: mode

    Conversion output format.

    Must be one of `plain`, `zlib`, or `json`

.. option:: infile

    Path (or URL, if :option:`--url` is specified) to file to be converted.

    If passed as ``-``, |soi| will attempt import of a plaintext or JSON
    inventory from ``stdin`` (incompatible with :option:`--url`).

.. option:: outfile

    *(Optional)* Path to desired output file. Defaults to same directory
    and main file name as input file but with extension
    |cour|\ .inv/.txt/.json\ |/cour|, as appropriate for the output format.

    A bare path is accepted here, using the default output
    file name/extension.

    If passed as ``-``, or if omitted when `infile` is passed as ``-``,
    |soi| will emit plaintext or JSON (but *not*
    zlib-compressed) inventory contents to ``stdout``.

**Flags**

.. option:: -h, --help

    Display `convert` help message and exit.

.. option:: -o, --overwrite

    If the output file already exists, overwrite without prompting
    for confirmation.

.. option:: -q, --quiet

    Suppress all status message output, regardless of success or failure.
    Useful for scripting/automation.  Implies :option:`--overwrite`.

.. option:: -u, --url

    Treat :option:`infile` as a URL for download. Cannot be used when
    :option:`infile` is passed as ``-``.

.. option:: -e, --expand

    Expand any abbreviations in `uri` or `dispname` fields before writing to output;
    see :ref:`here <syntax_shorthand>`. Cannot be specified with
    :option:`--contract`.

.. option:: -c, --contract

    Contract `uri` and `dispname` fields, if possible, before writing to output;
    see :ref:`here <syntax_shorthand>`. Cannot be specified with
    :option:`--expand`.
