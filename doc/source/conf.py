# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'sphobjinv'
copyright = '2016-2020, Brian Skinn'
author = 'Brian Skinn'

# The full version, including alpha/beta/rc tags
from sphobjinv import __version__ as release
version = ".".join(release.split(".")[:2])


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinxcontrib.programoutput",
    "sphinx_issues",
]

# napoleon configuration
napoleon_google_docstring = False
napoleon_use_rtype = False

# sphinx-issues config
issues_github_path = "bskinn/sphobjinv"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# No module name prepended to object titles in docs
add_module_names = False

# Highlighting style
pygments_style = "sphinx"

# Ignore package prefix when sorting modules
modindex_common_prefix = ["sphobjinv."]


# -- Common epilogue definition  ------------------------------------------------

rst_epilog = r"""
.. |extlink| image:: /_static/extlink.svg

.. |dag| replace:: :math:`^\dagger`

.. |None| replace:: :obj:`None`

.. |True| replace:: :obj:`True`

.. |False| replace:: :obj:`False`

.. |int| replace:: :obj:`int`

.. |float| replace:: :obj:`float`

.. |list| replace:: :obj:`list`

.. |tuple| replace:: :obj:`tuple`

.. |type| replace:: :obj:`type`

.. |str| replace:: :obj:`str`

.. |bytes| replace:: :obj:`bytes`

.. |bool| replace:: :obj:`bool`

.. |dict| replace:: :obj:`dict`

.. |re.compile| replace:: :func:`re.compile`

.. |re| replace:: :doc:`re <python:library/re>`

.. |Enum| replace:: :class:`~enum.Enum`

.. |isphx| replace:: :mod:`~sphinx.ext.intersphinx`

.. |Inventory| replace:: :class:`~sphobjinv.inventory.Inventory`

.. |license_txt| replace:: LICENSE.txt

.. _license_txt: https://github.com/bskinn/sphobjinv/blob/master/LICENSE.txt

.. |fuzzywuzzy| replace:: ``fuzzywuzzy``

.. _fuzzywuzzy: https://github.com/seatgeek/fuzzywuzzy

.. |python-Levenshtein| replace:: ``python-Levenshtein``

.. _python-Levenshtein: https://pypi.org/project/python-Levenshtein

.. |br| raw:: html

    <br />

.. |cour| raw:: html

    <span style="font-family:courier;font-size:90%">

.. |/cour| raw:: html

    </span>

.. |objects.inv| replace:: |cour|\ objects.inv\ |/cour|

.. |objects.txt| replace:: |cour|\ objects.txt\ |/cour|

.. |str.format| replace:: :meth:`str.format`

.. |isphxmap| replace:: ``intersphinx_mapping``

.. _isphxmap: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_mapping

.. |soi| raw:: html

    <span style="font-family:courier; font-size: 90%; font-weight: bold;">sphobjinv</span>

.. |stdin| replace:: |cour|\ stdin\ |/cour|

.. |stdout| replace:: |cour|\ stdout\ |/cour|

"""


# -- doctest setup code  --------------------------------------------


doctest_global_setup = """\
import os
from pathlib import Path
import shutil as sh

import sphobjinv as soi

# Should always be the doc root
_start_dir = Path().resolve()

# Create scratch dir if missing, and bind
_work_dir = Path('scratch')
_work_dir.mkdir(exist_ok=True)
_work_dir = _work_dir.resolve()

# Link ref to the attrs inventory
_res_inv = (_start_dir.parent / 'tests' / 'resource'
            / 'objects_attrs.inv')

# Scratch-clearing helper for later use
def _clear_files():
    for fp in [_ for _ in _work_dir.iterdir() if _.is_file()]:
        fp.unlink()

# Move to scratch, clear it, and copy in the attrs inv
os.chdir(str(_work_dir))
_clear_files()
sh.copy(str(_res_inv), str(Path()))


# Define helper(s) for running CLI commands

def cli_run(argstr, *, inp='', head=None):
    '''Run as if argstr was passed to shell.

    'inp' is input to pre-load to 'stdio_mgr' mocking
    of 'stdin.

    'head' is an integer, indicating the number
    of head lines to print.

    Can't handle quoted arguments.
    '''
    import sys

    import sphobjinv.cmdline as cli
    from stdio_mgr import stdio_mgr

    old_argv = sys.argv
    sys.argv = argstr.strip().split()

    with stdio_mgr(inp) as (i_, o_, e_):
        try:
            cli.main()
        except SystemExit:
            pass
        finally:
            sys.argv = old_argv

        output = o_.getvalue() + e_.getvalue()

    if head:
        output = '\\n'.join(output.splitlines()[:head])

    print(output)

def file_head(fn, *, head=None):
    '''Print the first 'head' lines of file at 'fn'; all if head==None.'''
    p = Path(fn)

    if not p.is_file():
        return "Not a file."

    with p.open() as f:
        text = f.read()

    # If head==None, then just returns a complete slice
    lines = text.splitlines()[:head]

    return "\\n".join(lines)

"""

doctest_global_cleanup = """\
_clear_files()

os.chdir(str(_start_dir))

"""


# -- Options for intersphinx  ------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}


# -- Options for linkcheck  --------------------------------------------------

linkcheck_anchors_ignore = [r"^L\d+$", r"^L\d+-L\d+$"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file basename
htmlhelp_basename = "sphobjinv"
