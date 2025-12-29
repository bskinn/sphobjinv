.. Description of sphobjinv-textconv commandline usage

Command-Line Usage: ``sphobjinv-textconv``
==========================================

.. program:: sphobjinv-textconv

``sphobjinv-textconv`` is intentionally implemented with very narrow
functionality, focused on simplifying use of |soi| as a `Git "textconv"
<https://git-scm.com/docs/gitattributes#_performing_text_diffs_of_binary_files>`__,
which is a mechanism for rendering binary files in a diff-able text format.
There are many `examples`__ of `clever application`__ of `textconv`__ in the
wild.

.. __: https://github.com/pixelb/crudini/issues/90
.. __: https://github.com/syntevosmartgit/textconv
.. __: https://stackoverflow.com/questions/55601430/how-to-pass-a-filename-argument-gitconfig-diff-textconv


Ultimately, a textconv requires three things:

1. A utility that takes in a file path as a single positional argument and emits
   a plaintext representation to |stdout|, such as |sphobjinv-textconv|.

2. An entry somewhere in Git config (system, user-global, per-repo, etc.)
   declaring a "diff driver" set up to use that utility as its |textconv|.
   Example::

      [diff "objects_inv"]
	      textconv = sphobjinv-textconv

   Note that the utility must be on path in all contexts where you wish to use
   it as a textconv.

3. An entry somewhere in |.gitattributes| (system, user-global, per-repo, etc.)
   that associates a particular file or glob pattern with the diff driver. Example::

      *.inv diff=objects_inv

With |sphobjinv-textconv| configured in this fashion as a textconv for Sphinx
inventory files, the following should all yield _nearly_ the same output.

Using ``sphobjinv convert``:

.. command-output:: sphobjinv convert plain objects_pdfminer.inv -
    :cwd: /../../tests/resource

Using ``sphobjinv-textconv`` (note the absence of blank lines between the shell
invocation and the inventory contents):

.. command-output:: sphobjinv-textconv objects_pdfminer.inv
    :cwd: /../../tests/resource

Using ``git show --textconv``:

.. command-output:: git show --textconv HEAD:tests/resource/objects_pdfminer.inv
    :cwd: /../../tests/resource

----


**Usage**

.. command-output:: sphobjinv-textconv --help
    :ellipsis: 4


**Positional Arguments**

.. option:: infile

    Path to file to be emitted to |stdout| in plaintext.

**Flags**

.. option:: -h, --help

    Display help message and exit.

.. option:: -v, --version

    Display brief package version information and exit.

.. versionadded:: ##VER##
