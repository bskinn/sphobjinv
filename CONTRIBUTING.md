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

There's no way I can fit a whole git **RESUME**
- Create new branch for the feature
- Link the main repo as `upstream` remote


## Tests

- pytest
- Defaults to only running tests not using network (local);
  do pytest --nonloc to test also  nonlocal things
- tox is set up not to be the everyday test runner,
  but instead to execute a detailed check of compatibility
  of Python and package dependency versions
- Maintain 100% test coverage in any PRs
  (discuss before using any pragma no cover)


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

