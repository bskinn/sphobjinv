.. Description of suggest commandline usage

Command-Line Usage: "suggest" Mode
==================================

.. program:: sphobjinv suggest

The |cour|\ suggest\ |/cour| subparser is used to query an inventory for objects
fuzzy-matching a given search string. Fuzzy-matching is carried out via the
|fuzzywuzzy|_ library, against the Restructured Text-like representation of each
object exposed by :attr:`SuperDataObj.as_rst <sphobjinv.data.SuperDataObj.as_rst>`:

.. doctest:: suggest_main

    >>> cli_run('sphobjinv suggest objects_attrs.inv instance')
    :py:exception:`attr.exceptions.FrozenInstanceError`
    :py:function:`attr.validators.instance_of`
    <BLANKLINE>

The |fuzzywuzzy|_ match score and the index of the object within the inventory can
be printed by passing the :option:`--score` and :option:`--index` options,
respectively:

.. doctest:: suggest_main

    >>> cli_run('sphobjinv suggest objects_attrs.inv instance -s -i')  # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
      Name                                                  Score    Index
    -----------------------------------------------------  -------  -------
    :py:exception:`attr.exceptions.FrozenInstanceError`      90        9
    :py:function:`attr.validators.instance_of`               90       23
    <BLANKLINE>

If too few or too many matches are returned, the reporting threshold can be changed
via :option:`--thresh`:

.. doctest:: suggest_main

    >>> cli_run('sphobjinv suggest objects_attrs.inv instance -s -i -t 48')  # doctest: +NORMALIZE_WHITESPACE
    <BLANKLINE>
      Name                                                  Score    Index
    -----------------------------------------------------  -------  -------
    :py:exception:`attr.exceptions.FrozenInstanceError`      90        9
    :py:function:`attr.validators.instance_of`               90       23
    :std:doc:`license`                                       51       47
    :py:function:`attr.filters.include`                      48       13
    <BLANKLINE>

Remote |objects.inv| files can be retrieved for inspection by passing the
:option:`--url` flag:

.. doctest:: suggest_main

    >>> cli_run('sphobjinv suggest https://github.com/bskinn/sphobjinv/raw/dev/sphobjinv/test/resource/objects_attrs.inv instance -u -t 48')  # doctest: +NORMALIZE_WHITESPACE
    :py:exception:`attr.exceptions.FrozenInstanceError`
    :py:function:`attr.validators.instance_of`
    :std:doc:`license`
    :py:function:`attr.filters.include`
    <BLANKLINE>

Note that |soi| only supports download of zlib-compressed |objects.inv| files by URL.
Plaintext download by URL is unreliable, presumably due to encoding problems.
If download of JSON files by URL is desirable, please
`submit an issue <https://github.com/bskinn/sphobjinv/issues>`__.

**Usage**

.. doctest:: suggest_usage

    >>> cli_run('sphobjinv suggest --help', head=3)
    usage: sphobjinv suggest [-h] [-a] [-i] [-s] [-t {0-100}] [-u] infile search
    <BLANKLINE>
    Fuzzy-search intersphinx inventory for desired object(s).

**Positional Arguments**

.. option:: infile

    Path (or URL, if :option:`--url` is specified) to file to be converted.

.. option:: search

    Search term for |fuzzywuzzy|_ matching

**Flags**

.. option:: -h, --help

    Display `suggest` help message and exit.

.. option:: -a, --all

    Display all search results without prompting, regardless of the number of hits.
    Otherwise, prompt if number of results exceeds
    :data:`sphobjinv.cmdline.SUGGEST_CONFIRM_LENGTH`.

.. option:: -i, --index

    Display the index position within the
    :attr:`Inventory.objects <sphobjinv.inventory.Inventory.objects>` list
    for each search result returned.

.. option:: -s, --score

    Display the |fuzzywuzzy|_ match score for each search result returned.

.. option:: -t, --thresh <#>

    Change the |fuzzywuzzy|_ match quality threshold (0-100; higher values
    yield fewer results). Default is specified in
    :data:`sphobjinv.cmdline.DEF_THRESH`.

.. option:: -u, --url

    Treat :option:`infile` as a URL for download.



