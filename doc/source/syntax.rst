.. Page describing objects.inv file syntax

Sphinx objects.inv v2 Syntax
============================

After decompression, "version 2" Sphinx |objects.inv| files follow a syntax
that, to the best of this author's ability to determine, is not included in the
Sphinx documentation. The below syntax is believed to be accurate as of May 2024
(Sphinx v7.3.7). It is based on inspection of |objects.inv| files "in the
wild" and of the Sphinx inventory object `parsing regex`_.

Based upon a quick ``git diff`` of the `Sphinx repository
<https://github.com/sphinx-doc/sphinx>`__, it is thought to be valid for all
Sphinx versions >=1.0b1 that make use of this "version 2" |objects.inv| format.

**NOTE** that previous versions of the syntax presented here have been
shown to be inaccurate:

  * It *is* permitted for the |{name}|_ field to contain whitespace (see :issue:`181`).

  * It *is* permitted for the |{role}|_ field to contain a colon (see :issue:`256`).

The descriptions below have been updated to reflect this and to provide more
detailed information on the constraints governing each field of an |objects.inv|
data line.

----

**The first line** `must be exactly
<https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/util/inventory.py#L90-L91>`__:

.. code-block:: none

    # Sphinx inventory version 2

----

**The second and third lines** `must obey
<https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/util/inventory.py#L126-L127>`__
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
<https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/util/inventory.py#L128-L130>`__
the string ``zlib`` somewhere within it, but for consistency it should be exactly:

.. code-block:: none

    # The remainder of this file is compressed using zlib.

----

**All remaining lines** of the file are the objects data, each laid out in the
`following syntax
<https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/util/inventory.py#L186-L188>`__:

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
    second and third/last colons; or, between the first and second/last colons if
    using the |defdom|_).

    Note that the role MAY contain a colon, as occurs with the
    |rst-directive-option|_ directive in the Sphinx docs.

    **Constraints**

    * **MUST** have nonzero length

    * **MUST** match a role defined in the domain referenced by ``{domain}``

    * **MUST NOT** contain whitespace

      * **RECOMMENDED** to consist of only ASCII word characters (``a-z``, ``A-Z``,
        ``0-9``, and ``_``)

.. _{priority}:

``{priority}``
    Flag for `placement in search results
    <https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/domains/__init__.py#L378-L389>`__. Most will be ``1`` (standard priority) or
    ``-1`` (omit from results) for documentation built by Sphinx;
    values of ``0`` (higher priority) or ``2`` (lower priority) may also occur.

    To note, as of Jan 2022 this value is **not** used by ``intersphinx``;
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
Python 3.12 |objects.inv|, broken out field-by-field:

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
    <https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/util/inventory.py#L178-L180>`__
    with ``$``. |br| |br|

 #. If |{dispname}|_ is identical to |{name}|_, it is `stored
    <https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/util/inventory.py#L184-L185>`__
    as ``-``.

Thus, a standard |isphx| reference to this method would take the form:

.. code-block:: none

    :py:meth:`str.join`

The leading ``:py`` here could be omitted if ``py`` is the default domain.

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

.. _prio_js_search: https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/themes/basic/static/searchtools.js#L28-L46

.. |prio_py_search| replace:: here

.. _prio_py_search: https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/search/__init__.py#L344-L345

.. |sphinx_uri_issue| replace:: sphinx-doc/sphinx#7096

.. _sphinx_uri_issue: https://github.com/sphinx-doc/sphinx/issues/7096

.. |{name}| replace:: ``{name}``

.. |{domain}| replace:: ``{domain}``

.. |{role}| replace:: ``{role}``

.. |{priority}| replace:: ``{priority}``

.. |{uri}| replace:: ``{uri}``

.. |{dispname}| replace:: ``{dispname}``

.. |rst-directive-option| replace:: ``:rst:directive:option:``

.. _rst-directive-option: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#directive-rst-directive-option

.. _parsing regex: https://github.com/sphinx-doc/sphinx/blob/ac3f74a3e0fbb326f73989a16dfa369e072064ca/sphinx/util/inventory.py#L134-L135
