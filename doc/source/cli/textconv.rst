.. Description of sphobjinv-textconv commandline usage

Command-Line Usage: |soi-textconv|
===================================

.. program:: |soi-textconv|

Terse syntax command to convert |objects.inv| to |stdout|. Extends
:code:`git diff`. Comparing against partially binary
|objects.inv| versions, produces useful results.

Rather than *These two binary files differ*

Unlike |soi|, |soi-textconv| coding style is ``adapt to survive``.
Regardless of what's thrown at it, does what it can.

Difference

- when an inventory file is piped in from |stdin|, specifying "-" is optional

- checks |stdin| even before parsing cli arguments

----

**Usage**

.. command-output:: sphobjinv-textconv --help
    :ellipsis: 4

.. versionadded:: 2.4.0

.. seealso::

   Step by step configuration, usage, and code samples

   :doc:`git_diff`

**Positional Arguments**

.. option:: infile

    Path (or URL, if :option:`--url` is specified) to file to be converted.

    If passed as ``-``, |soi-textconv| will attempt import of a plaintext or JSON
    inventory from |stdin| (incompatible with :option:`--url`).

**Flags**

.. option:: -h, --help

    Display help message and exit.

.. option:: -u, --url

    Treat :option:`infile` as a URL for download. Cannot be used when
    :option:`infile` is passed as ``-``.

.. option:: -e, --expand

    Expand any abbreviations in `uri` or `dispname` fields before writing to output;
    see :ref:`here <syntax_shorthand>`.

**Examples**

Remote URL

.. code-block:: shell

   export URL="https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv"
   sphobjinv-textconv "$URL"

Local URL

.. code-block:: shell

   sphobjinv-textconv --url "file:///home/pepe/Downloads/objects.inv"

Piping in compressed inventories is not allowed

.. code-block:: shell

   sphobjinv-textconv "-" < objects.inv

^^ BAD ^^

.. code-block:: shell

   export URL="https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv"
   sphobjinv-textconv "-" < "$URL"

plain text

.. code-block:: shell

   export URL="https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv"
   sphobjinv convert -uq plain "$URL" "-" | sphobjinv-textconv

JSON

.. code-block:: shell

   sphobjinv-textconv < objects.json

Expanding `uri` or `dispname` fields

.. code-block:: shell

   sphobjinv-textconv -e objects.inv

.. caution:: Caveat

   When an inventory is piped in from stdin, ``-e`` option is ignored
