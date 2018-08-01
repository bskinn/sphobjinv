.. Info on speedups from python-Levenshtein

Speeding up "suggest" with python-Levenshtein
=============================================

|soi| uses |fuzzywuzzy|_ for fuzzy-match searching of object
names/domains/roles as part of the
:meth:`~sphobjinv.inventory.Inventory.suggest` functionality.

(maybe link above instead to the CLI page?)

MORE EXPLANATION
 fuzzywuzzy has a built-in, pure-Python fuzzy search algorithm, but
 it also can use python-Levenshtein, a Python C extension providing
 similar functionality. Thus, |soi| has been implemented with
 python-Levenshtein as an *optional* dependency.


Performance Benchmark
---------------------

[change to not mention chart until later?]
The chart below presents one dataset illustrating the performance enhancement
that can be obtained by installing python-Levenshtein.
The timings plotted here are from execution of the `timeit` module in the
Python standard library on the `.suggest` thing, using the following
command(s):

.. code::

   ... hopefully no doctest?

[CHART HERE]

The testing was run over the set of fifty-two
|cour|\ objects_xxx.inv\ |/cour| files found
`here <https://github.com/bskinn/sphobjinv/tree/
6c1f22e40dc3d129485462aec05adbed2ff40ab8/sphobjinv/test/resource>`__,
which contain widely varying numbers of objects :math:`n`.

Unsurprisingly, larger inventories require more time to search;
also relatively unsurprisingly, the time required appears to be
roughly :math:`O(n)` (the fuzzy search must be performed once
on the [ADD ISPHX TO as_rst HERE] representation of each object).


Variations in Behavior
----------------------

NOTE THAT MATCHING SCORES DIFFER W/ AND W/O LEVENSHTEIN
 (cf. PyPI project README)
 Show code examples? Might not be possible to doctest them,
 though some pre-test-block magic might enable?
 Or just state the version of fuzzywuzzy and pL, and the
 exact file used, and include the p-L results without
 doctesting them. (Should still be able to doctest
 the p-L-free results. Depends on the dev environment
 not having p-L installed, though.)



Installation Considerations
---------------------------

On Linux, simple installation via
|cour|\ pip install python-Levenshtein\ |/cour| should work
properly in the vast majority of cases. I would anticipate
this to work smoothly for MacOS as well, but I don't have
first-hand	indication (`yet? <https://twitter.com/btskinn/status/1024503861443276801>`__)
that it works.

On Windows, as of this writing
`no binary wheel is available on PyPI <https://pypi.org/project/python-Levenshtein/0.12.0/#files>`__,
so the easiest way to install p-L is to download the wheel from
`Christoph Gohlke's repository <https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-levenshtein>`__.
Just make sure to match the Python version and your CPU type (win32 vs win_amd64).

