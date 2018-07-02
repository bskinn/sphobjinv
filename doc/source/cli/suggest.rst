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

    TEXT

.. option:: search

    SEARCH TEXT

**Flags**

.. option:: -h, --help

    ...

.. option:: -a, --all

    ...

.. option:: -i, --index

    ...

.. option:: -s, --score

    ...

.. option:: -t, --thresh

    ...

.. option:: -u, --url

    ...



