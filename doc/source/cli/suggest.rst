.. Description of suggest commandline usage

Command-Line Usage: "suggest" Subcommand
========================================

.. program:: sphobjinv suggest

The "suggest" subcommand is used to query an inventory for
objects fuzzy-matching a given search string. The search string is matched
against the reStructuredText-like representation of each object in the
|objects.inv|, and all objects with a score above a set threshold are printed:

.. command-output:: sphobjinv suggest objects_attrs.inv instance
   :cwd: /../../tests/resource

The match score and the index of the object within the inventory can
be printed by passing the :option:`--score` and :option:`--index` options,
respectively:

.. command-output:: sphobjinv suggest objects_attrs.inv instance -s -i
   :cwd: /../../tests/resource

If too few or too many matches are returned, the reporting threshold can be changed
via :option:`--thresh`:

.. command-output:: sphobjinv suggest objects_attrs.inv instance -s -i -t 48
   :cwd: /../../tests/resource

Remote |objects.inv| files can be retrieved for inspection by passing the
:option:`--url` flag:

.. command-output:: sphobjinv suggest https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv instance -u -t 48
   :cwd: /../../tests/resource

The URL provided **MUST** have the leading protocol specified (here,
|cour|\ https\ ://\ |/cour|).

It is usually not necessary to locate the |objects.inv| file before running |soi|;
for most Sphinx documentation sets, if you provide a URL to any page in the docs,
it will automatically find and use the correct |objects.inv|:

.. command-output:: sphobjinv suggest -u https://sphobjinv.readthedocs.io/en/stable/cli/convert.html compress
   :cwd: /../../tests/resource

|soi| only supports download of zlib-compressed |objects.inv| files by URL.
Plaintext download by URL is unreliable, presumably due to encoding problems.
If download of JSON files by URL is desirable, please
`submit an issue <https://github.com/bskinn/sphobjinv/issues>`__.

.. versionadded:: 2.1
    The |soi| CLI can now read JSON and plaintext inventories from ``stdin``
    by passing the special ``-`` argument for `infile`:

    .. command-output:: sphobjinv suggest -s - valid < objects_attrs.txt
        :cwd: /../../tests/resource
        :shell:

**Usage**

.. command-output:: sphobjinv suggest --help
   :ellipsis: 4

**Positional Arguments**

.. option:: infile

    Path (or URL, if :option:`--url` is specified) to file to be searched.

    If passed as ``-``, |soi| will attempt import of a plaintext or JSON
    inventory from ``stdin``. This is incompatible with :option:`--url`,
    and automatically enables :option:`--all`.

.. option:: search

    Search term for matching against inventory objects.

**Flags**

.. option:: -h, --help

    Display `suggest` help message and exit.

.. option:: -a, --all

    Display all search results without prompting, regardless of the number of hits.
    Otherwise, prompt if number of results exceeds
    :attr:`~sphobjinv.cli.parser.PrsConst.SUGGEST_CONFIRM_LENGTH`.

.. option:: -i, --index

    Display the index position within the
    :attr:`Inventory.objects <sphobjinv.inventory.Inventory.objects>` list
    for each search result returned.

.. option:: -s, --score

    Display the match score for each search result returned.

.. option:: -t, --thresh <#>

    Change the match quality threshold (0-100; higher values
    yield fewer results). Default is specified in
    :attr:`~sphobjinv.cli.parser.PrsConst.DEF_THRESH`.

.. option:: -u, --url

    Treat :option:`infile` as a URL for download. Cannot be used when
    :option:`infile` is passed as ``-``.
