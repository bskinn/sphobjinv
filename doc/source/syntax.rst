.. Page describing objects.inv file syntax

Sphinx objects.inv v2 Syntax
============================

After decompression, "version 2" Sphinx |objects.inv| files
follow a syntax that, to the best of this author's ability to determine,
is not included in the Sphinx documentation. The below
syntax is believed to be accurate as of Feb 2021 (Sphinx v3.4.3).

Based upon a quick ``git diff`` of the `Sphinx repository
<https://github.com/sphinx-doc/sphinx>`__, it is thought to be valid for all
Sphinx versions >=1.0b1 that make use of this "version 2" |objects.inv| format.

**NOTE** that the previous version of the syntax presented here has been
shown to be inaccurate (see :issue:`181`), in that it *is*
permitted for the |{name}|_ field to contain whitespace.
The descriptions below have been updated to reflect this and to provide
more detailed information on the constraints governing each field
of an |objects.inv| data line.

----

**The first line** `must be exactly
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L105-L106>`__:

.. code-block:: none

    # Sphinx inventory version 2

----

**The second and third lines** `must obey
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L133-L134>`__
the template:

.. code-block:: none

    # Project: <project name>
    # Version: <full version number>

The version number should *not* include a leading "v".

.. _syntax-mouseover-example:

The above project name and version are used to populate mouseovers for
the |isphx| cross-references:

    .. image:: _static/mouseover_example.png

----

**The fourth line** `must contain
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L136-L137>`__
the string ``zlib`` somewhere within it, but for consistency it should be exactly:

.. code-block:: none

    # The remainder of this file is compressed using zlib.

----

**All remaining lines** of the file are the objects data, each laid out in the
`following syntax
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L188-L190>`__:

.. code-block:: none

    {name} {domain}:{role} {priority} {uri} {dispname}

.. _{name}:

``{name}``

    The object name used when cross-referencing the object (falls between the
    backticks).

    **Constraints**

    * **MUST** have nonzero length

    * **MUST NOT** start with ``#``

    * **SHOULD** have no leading or trailing whitespace

    * **MAY** contain internal whitespace

.. _{domain}:

``{domain}``
    The Sphinx domain used when cross-referencing the object (falls between
    the first and second colons; omitted if using the |defdom|_).

    **Constraints**

    * **MUST** have nonzero length

    * **MUST** match a built-in or installable Sphinx domain

    * **MUST NOT** contain whitespace or a colon

      * **RECOMMENDED** to contain only ASCII word characters (``a-z``, ``A-Z``,
        ``0-9``, and ``_``)

.. _{role}:

``{role}``
    The Sphinx role used when cross-referencing the object (falls between the
    second and third colons; or, between the first and second colons if
    using the |defdom|_).

    **Constraints**

    * **MUST** have nonzero length

    * **MUST** match a role defined in the domain referenced by ``{domain}``

    * **MUST NOT** contain whitespace or a colon

      * **RECOMMENDED** to consist of only ASCII word characters (``a-z``, ``A-Z``,
        ``0-9``, and ``_``)

.. _{priority}:

``{priority}``
    Flag for `placement in search results
    <https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/domains/
    __init__.py#L319-L325>`__. Most will be ``1`` (standard priority) or
    ``-1`` (omit from results) for documentation built by Sphinx.

    To note, as of Feb 2021 this value is **not** used by ``intersphinx``;
    it is only used internally within the search function of the static webpages
    built *by Sphinx* (|prio_py_search|_ and |prio_js_search|_). Thus, custom
    inventories likely **MAY** use this field for arbitrary content, if desired,
    as long as the integer constraint is observed.
    Such use *would* run the risk of a future change to Sphinx/intersphinx
    breaking compatibility with |objects.inv| files
    having non-standard |{priority}|_ values.

    **Constraints**

    * **MUST** have nonzero length

    * **MUST** be a positive or negative integer, or zero,
      *without* a decimal point

    * **MUST NOT** contain whitespace (implicit in the integer constraint)

.. _{uri}:

``{uri}``
    Relative URI for the location to which cross-references will point.
    The base URI is taken from the relevant element of the |isphxmap|
    configuration parameter in ``conf.py``.

    **Constraints**

    * **MAY** have zero length, but typically has nonzero length

      * A zero-length |{uri}|_ can occur for the
        root/index documentation page in certain instances;
        see |sphinx_uri_issue|_

    * **MUST NOT** contain whitespace

.. _{dispname}:

``{dispname}``
    Default cross-reference text to be displayed in compiled documentation.

    **Constraints**

    * **MUST** have nonzero length

    * **MAY** contain internal whitespace (leading/trailing whitespace
      is ignored)

Unicode characters appear to be valid for all fields except
|{uri}|_ (where they are `specifically forbidden <https://stackoverflow.com/a/1916747/4376000>`__)
and |{priority}|_.
However, it is **RECOMMENDED** that they *only* be used in |{dispname}|_,
as their use in |{name}|_, |{domain}|_ and |{role}|_ would complicate construction
of cross-references from other documentation source.

----

**For illustration**, the following is the entry for the
:meth:`join() <str.join>` method of the :class:`str` class in the
Python 3.9 |objects.inv|, broken out field-by-field:

.. code-block:: none

    str.join py:method 1 library/stdtypes.html#$ -

    {name}      = str.join
    {domain}    = py
    {role}      = method
    {priority}  = 1
    {uri}       = library/stdtypes.html#$
    {dispname}  = -


.. _syntax_shorthand:

The above illustrates two shorthand notations that were introduced to shrink the
size of the inventory file:

 #. If |{uri}|_ has an anchor (technically a "`fragment identifier
    <https://en.wikipedia.org/wiki/Fragment_identifier>`__," the portion
    following the ``#`` symbol) and the tail of the anchor is identical to
    |{name}|_, that tail is `replaced
    <https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L180-L182>`__
    with ``$``. |br| |br|

 #. If |{dispname}|_ is identical to |{name}|_, it is `stored
    <https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L186-L187>`__
    as ``-``.

Thus, a standard |isphx| reference to this method would take the form (the leading
``:py`` could be omitted if ``py`` is the default domain):

.. code-block:: none

    :py:meth:`str.join`

The cross-reference would show as :meth:`str.join` and link to the relative URI:

.. code-block:: none

    library/stdtypes.html#str.join

----

**Other intersphinx Syntax Examples**

To show as only :meth:`~str.join`:

.. code-block:: none

   :py:meth:`~str.join`

To suppress the hyperlink as in :meth:`!str.join`:

.. code-block:: none

   :py:meth:`!str.join`

To change the cross-reference text and omit the trailing parentheses
as in :obj:`This is join! <str.join>`:

.. code-block:: none

   :py:obj:`This is join! <str.join>`



.. ## Definitions ##

.. |defdom| replace:: default domain

.. _defdom: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html

.. |prio_js_search| replace:: here

.. _prio_js_search: https://github.com/sphinx-doc/sphinx/blob/241577f65eea94a08944bf096bd704b495282373/sphinx/themes/basic/static/searchtools.js#L26-L43

.. |prio_py_search| replace:: here

.. _prio_py_search: https://github.com/sphinx-doc/sphinx/blob/241577f65eea94a08944bf096bd704b495282373/sphinx/search/__init__.py#L332

.. |sphinx_uri_issue| replace:: sphinx-doc/sphinx#7096

.. _sphinx_uri_issue: https://github.com/sphinx-doc/sphinx/issues/7096

.. |{name}| replace:: ``{name}``

.. |{domain}| replace:: ``{domain}``

.. |{role}| replace:: ``{role}``

.. |{priority}| replace:: ``{priority}``

.. |{uri}| replace:: ``{uri}``

.. |{dispname}| replace:: ``{dispname}``
