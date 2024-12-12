.. Description of configure git diff support for inventory files

Integration -- git diff
========================

.. program:: git diff

|soi-textconv| converts .inv files to plain text sending the
output to |stdout|.

.. code-block:: shell

   sphobjinv-textconv objects.inv

Which is equivalent to

.. code-block:: shell

   sphobjinv convert plain objects.inv -

Convenience aside, why the redundant CLI command, |soi-textconv|?

To compare changes to a |objects.inv| file, :code:`git diff` won't
produce a useful result without configuration. And git only accepts a
CLI command with:

- one input, the INFILE path

- sends output to |stdout|

Usage
------

Initialize git
"""""""""""""""

.. code-block:: shell

   git init
   git config user.email test@example.com
   git config user.name "a test"

Configure git
""""""""""""""

``git diff`` is really useful, so it's time to configure git

There is no CLI command to configure git for us.

In ``.git/config`` (or $HOME/.config/git/config) append,

.. code-block:: text

   [diff "inv"]
   	textconv = [absolute path to venv bin folder]/sphobjinv-textconv

Note has one tab, not whitespace(s)

In ``.gitattributes`` append,

.. code-block:: text

   *.inv binary diff=inv

Example
--------

Make one commit
""""""""""""""""

Commit these files:

- objects_attrs.inv

- objects_attrs.txt

- .gitattributes

.. code-block:: shell

   git add .
   git commit --no-verify --no-gpg-sign -m "test textconv"

Make a change to ``objects_attrs.inv``
"""""""""""""""""""""""""""""""""""""""

By shell

.. code-block:: shell

   URL="https://github.com/bskinn/sphobjinv/raw/main/tests/resource/objects_attrs.inv"
   wget "$URL"
   sphobjinv convert plain -qu "$URL" objects_attrs.txt
   export APPEND_THIS="attrs.validators.set_cheat_mode py:function 1 api.html#$ -"
   echo "$APPEND_THIS" >> objects_attrs.txt
   sphobjinv convert zlib -qu objects_attrs.txt objects_attrs.inv

By python code

.. versionadded:: 2.4.0
    Append a line to .inv (compressed) inventory

    .. doctest:: append_a_line

       >>> from pathlib import Path
       >>> from sphobjinv import DataObjStr
       >>> from sphobjinv.cli.load import import_infile
       >>> from sphobjinv.cli.write import write_plaintext
       >>>
       >>> remote_url = (
       ...     "https://github.com/bskinn/sphobjinv/"
       ...     "raw/main/tests/resource/objects_attrs.inv"
       ... )
       >>> cli_run(f'sphobjinv convert plain -qu {remote_url} objects_attrs.txt')
       <BLANKLINE>
       >>> path_dst_dec = Path('objects_attrs.txt')
       >>> path_dst_cmp = Path('objects_attrs.inv')
       >>> dst_dec_path = str(path_dst_dec)
       >>> path_dst_dec.is_file()
       True
       >>> inv_0 = import_infile(dst_dec_path)
       >>> obj_datum = DataObjStr(
       ...     name="attrs.validators.set_cheat_mode",
       ...     domain="py",
       ...     role="function",
       ...     priority="1",
       ...     uri="api.html#$",
       ...     dispname="-",
       ... )
       >>> inv_0.objects.append(obj_datum)
       >>> write_plaintext(inv_0, dst_dec_path)
       >>> cli_run('sphobjinv convert -q zlib objects_attrs.txt objects_attrs.inv')
       <BLANKLINE>
       >>> path_dst_cmp.is_file()
       True

Show the diff
""""""""""""""

To see the changes to objects_attrs.inv

.. code-block:: shell

   git diff HEAD objects_attrs.inv 2>/dev/null

Without |soi-textconv|, *These two binary files differ*

With |soi-textconv| configured

.. code-block:: text

   diff --git a/objects.inv b/objects.inv
   index 85189bd..65cc567 100644
   --- a/objects.inv
   +++ b/objects.inv
   @@ -131,4 +131,5 @@ types std:doc -1 types.html Type Annotations
    validators std:label -1 init.html#$ Validators
    version-info std:label -1 api.html#$ -
    why std:doc -1 why.html Why not…
   +attrs.validators.set_cheat_mode py:function 1 api.html#$ -

The last line contains <whitespace><newline> rather than <newline>

The 2nd line changes every time

:code:`2>/dev/null` means suppress |stderr|
