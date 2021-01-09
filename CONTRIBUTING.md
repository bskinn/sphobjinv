Welcome!
--------

Thanks for your interest in contributing to `sphobjinv`!
The aim of this document is to provide the information you need
to get started smoothly on a contribution.

If you have any questions, please drop me a line on Twitter
([@btskinn](https://twitter.com/btskinn)) or open an
[issue](https://github.com/bskinn/sphobjinv/issues).


Table of Contents
-----------------

<!--TOC-->

- [Project Setup](#project-setup)
- [Working with git](#working-with-git)
- [Tests](#tests)
- [Linting](#linting)
- [Continuous Integration](#continuous-integration)
- [Documentation](#documentation)
- [Type Hints](#type-hints)
- [CHANGELOG](#changelog)
- [Issue & PR Templates](#issue--pr-templates)
- [License](#license)

<!--TOC-->


## Project Setup

Start by forking the repo and cloning locally:

```
$ git clone https://github.com/{you}/sphobjinv
```

Then, create a virtual environment for the project,
in whatever location you prefer. Any Python interpreter 3.6+ *should* work fine.

I prefer to use `virtualenv` and create in `./env`:

```
$ python3.9 -m virtualenv env --prompt="(sphobjinv) "
```

Activate the environment:

```
=== Linux/Mac
$ source env/bin/activate

=== Windows
> env\scripts\activate
```

The next step is to upgrade/install the development requirements:

```
(sphobjinv) $ python -m pip install -U pip setuptools wheel
(sphobjinv) $ pip install -r requirements-dev.txt
```

Finally, you'll need to build the Sphinx docs,
as some of the tests interact with them:

```
(sphobjinv) $ cd doc
(sphobjinv) doc $ make html
```


## Working with git

There's no way I can fit a whole git tutorial in here, so this
just highlights a couple of key functionalities you'll need.

First, always hack on a bugfix or feature in a new branch:

```
$ git checkout -b description-of-change
```

This makes it a lot simpler to get your repo fork up to date
when `master` inevitably moves on after you clone the repo.

To bring your fork's `master` up to date, you first need to
add the main repo as a new git remote (one-time task):

```
$ git remote add upstream https://github.com/bskinn/sphobjinv
```

Then, any time you need to refresh the fork's master:

```
$ git fetch --all
$ git checkout master
$ git merge upstream/master  # (*should* merge without incident)
$ git push
```


## Tests

`sphobjinv` uses the [`pytest`](https://github.com/pytest-dev/pytest)
framework for most of its automated tests. From a properly configured
virtual environment, a simple no-arguments invocation is all
that is required:

```
$ pytest
```

The test suite defaults to running only local tests,
those that do **NOT** require network access. To include
the nonlocal tests, run with the `--nonloc` flag:

```
$ pytest --nonloc
```

At minimum, please add/augment the test suite as necessary
to maintain 100% test coverage. To the extent possible,
please go beyond this and add tests that check potential edge cases,
bad/malformed/invalid inputs, etc. 

There are some situations where it may make sense to use a
`# pragma: no cover` to ignore coverage on certain line(s) of code.
Please start a discussion in the issue or PR comments before
adding such a pragma.

Note that while [`tox`](https://github.com/tox-dev/tox/) *is*
configured for the project, it is **not** set up to be an everyday test runner.
Instead, it's used to execute a matrix of test environments
checking for the compatibility of different Python and  dependency
versions. You can run it if you want, but you'll need
working versions of all of Python 3.6 through 3.10
installed and on `PATH` as `python3.6`, `python3.7`, etc.
The nonlocal test suite is run for each `tox` environment, so
use at most two parallel sub-processes to avoid oversaturating
your network bandwidth; e.g.:

```
$ tox -rp2
```


## Linting

- Bunch of stuff in flake8 (tox -e flake8)
- Docstring existence check via interrogate
  (tox -e interrogate)
- Discuss before using any noqa or exclusions


## Continuous Integration

- GHA for basic test runs on Linux, all commits
- AP for extensive testing, only on PRs to master/stable
  and on release branches


## Documentation

- Docstrings on everything---numpy style
- Add/change for functionality changes
- make clean html for POSIX/Mac
- make html -Ean for Windows
- make doctest
- make linkcheck


## Type Hints

- Future issue is adding types across the project
  (would be a great contribution?)


## CHANGELOG

- Anything that touches code or tests definitely
  needs a CHANGELOG bullet
- Other changes of note (packaging, building, testing/linting
  tooling, tool settings, etc.) may warrant a CHANGELOG bullet;
  depends


## Issue & PR Templates

- For most bug reports and feature requests,
  should use
- Use judgment, though -- if the templates don't
  really fit, don't worry about using them.


## License

All contributions will take on the MIT License of the project at large.

