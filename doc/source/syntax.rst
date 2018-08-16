.. Page describing objects.inv file syntax

Sphinx objects.inv v2 Syntax
============================

After decompression, "version 2" Sphinx |objects.inv| files
follow a syntax that, to the best of this author's ability to determine,
is completely undocumented. The below
syntax is believed to be accurate as of Jun 2018 (Sphinx v1.7.4).
Based upon a quick ``git diff`` of the `Sphinx repository
<https://github.com/sphinx-doc/sphinx>`__, it is thought to be accurate for all
Sphinx versions >=1.0b1 that make use of this "version 2" |objects.inv| format.

**The first line** `must be exactly
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L105-L106>`__:

.. code-block:: none

    # Sphinx inventory version 2

**The second and third lines** `must obey
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L133-L134>`__
the template:

.. code-block:: none

    # Project: <project name>
    # Version: <full version number>

.. _syntax-mouseover-example:

The above project name and version are used to populate mouseovers for
the |isphx| cross-references:

    .. image:: _static/mouseover_example.png

**The fourth line** `must contain
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L136-L137>`__
the string 'zlib' somewhere in it, but for the purposes of consistency it should
be exactly:

.. code-block:: none

    # The remainder of this file is compressed using zlib.


**All remaining lines** of the file are the objects data, each laid out in the
`following syntax
<https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L188-L190>`__:

.. code-block:: none

    {name} {domain}:{role} {priority} {uri} {dispname}

``{name}``
    The object name used when cross-referencing the object (falls between the
    backticks)

``{domain}``
    The Sphinx domain used when cross-referencing the object (falls between
    the first and second colons; omitted if using the |defdom|_)

``{role}``
    The Sphinx role used when cross-referencing the object (falls between the
    second and third colons; or, between the first and second colons if
    using the |defdom|_)

``{priority}``
    Flag for `placement in search results
    <https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/domains/
    __init__.py#L319-L325>`__. Most will be 1 (standard priority) or
    -1 (omit from results)

``{uri}``
    Relative URI for the location to which cross-references will point.
    The base URI is taken from the relevant element of the |isphxmap|
    configuration parameter of ``conf.py``.

``{dispname}``
    Default cross-reference text to be displayed in compiled documentation.

.. note::

    The above fields MUST NOT contain spaces,
    except for ``{dispname}`` which MAY contain them.

**For illustration**, the following is the entry for the
:meth:`join() <str.join>` method of the :class:`str` class in the
Python 3.5 |objects.inv|, broken out field-by-field:

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

 #. If ``{uri}`` has an anchor (technically a "`fragment identifier
    <https://en.wikipedia.org/wiki/Fragment_identifier>`__," the portion
    following the ``#`` symbol) and the tail of the anchor is identical to
    ``{name}``, that tail is `replaced
    <https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L180-L182>`__
    with ``$``. |br| |br|

 #. If ``{dispname}`` is identical to ``{name}``, it is `stored
    <https://github.com/sphinx-doc/sphinx/blob/f7b3292d87e9a2b7eae0b4ef72e87779beefc699/sphinx/util/inventory.py#L186-L187>`__
    as ``-``.

Thus, a standard |isphx| reference to this method would take the form (the leading
``:py`` could be omitted if ``py`` is the default domain):

.. code-block:: none

    :py:meth:`str.join`

The cross-reference would show as :meth:`str.join` and link to the relative URI:

.. code-block:: none

    library/stdtypes.html#str.join

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



.. |defdom| replace:: default domain

.. _defdom: http://www.sphinx-doc.org/en/stable/domains.html

