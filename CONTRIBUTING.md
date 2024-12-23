Welcome!  <!-- omit in toc -->
--------

Thanks for your interest in contributing to `sphobjinv`!
The aim of this document is to provide the information you need
to get started smoothly on a contribution.

If you have any questions, please drop me a line on Mastodon
([@btskinn@fosstodon.org](https://fosstodon.org/@btskinn)) or open an
[issue](https://github.com/bskinn/sphobjinv/issues).


Table of Contents <!-- omit in toc -->
-----------------

<!--TOC-->

- [Project Setup](#project-setup)
- [Working with git](#working-with-git)
- [Tests](#tests)
- [Code Autoformatting](#code-autoformatting)
- [Linting](#linting)
- [Type Hints](#type-hints)
- [Documentation](#documentation)
- [Continuous Integration](#continuous-integration)
- [CHANGELOG](#changelog)
- [Issue and PR Templates](#issue-and-pr-templates)
- [License](#license)

<!--TOC-->


## Project Setup

Start by forking the repo on GitHub and cloning locally:

```bash
$ git clone https://github.com/{you}/sphobjinv
```

Then, create a virtual environment for the project, in whatever location you
prefer. Any Python interpreter 3.9+ *should* work fine.

I prefer to use `virtualenv` and create in `./env`:

```bash
$ python3.12 -m virtualenv env --prompt="sphobjinv"
```

Activate the environment:

```bash
# Linux/Mac
$ source env/bin/activate

# Windows
> env\scripts\activate
```

The next step is to upgrade/install the development requirements:

```bash
(sphobjinv) $ python -m pip install -U pip setuptools wheel
(sphobjinv) $ pip install -r requirements-dev.txt
```

Finally, you'll need to build the Sphinx docs locally, as some of the tests
interact with them:

```bash
(sphobjinv) $ cd doc
(sphobjinv) doc $ make html
```


## Working with git

There's no way I can fit a whole git tutorial in here, so this just highlights a
couple of key functionalities you'll need.

First, always hack on a bugfix or feature in a new branch:

```bash
$ git checkout -b description-of-change
```

This makes it a lot simpler to get your repo fork up to date after `main`
receives further commits.

To bring your fork's `main` up to date, you first need to add the main repo as a
new git remote (one-time task per clone):

```bash
$ git remote add upstream https://github.com/bskinn/sphobjinv
```

Then, any time you need to refresh the fork's `main`:

```bash
$ git fetch --all
$ git checkout main
$ git merge upstream/main   # (should merge without incident)
$ git push                  # (should push to your fork without incident)
```


## Tests

`sphobjinv` uses the [`pytest`](https://github.com/pytest-dev/pytest) framework
for most of its automated tests. From a properly configured virtual environment,
a simple no-arguments invocation is all that is required:

```bash
$ pytest
```

The test suite defaults to running only local tests, those that do **NOT**
require network access. To include the nonlocal tests, run with the `--nonloc`
flag:

```bash
$ pytest --nonloc
```

When putting together a PR, at minimum, please add/augment the test suite as
necessary to maintain 100% test coverage. To the extent possible, please go
beyond this and add tests that check potential edge cases, bad/malformed/invalid
inputs, etc. For bugfixes, add one or more focused regression tests that cover
the bug behavior being fixed.

PRs that add
[xfail tests for existing bugs](https://blog.ganssle.io/articles/2021/11/pytest-xfail.html)
are also welcomed.

There are some situations where it may make sense to use a `# pragma: no cover`
to ignore coverage on certain line(s) of code. Please start a discussion in the
issue or PR comments before adding such a pragma.

Note that while [`tox`](https://tox.wiki/en/latest/) *is* configured for the
project, it is **not** set up to be an everyday test runner. Instead, its
purpose for testing is to execute an extensive matrix of test environments
checking for the compatibility of different Python and dependency versions. You
can run it if you want, but you'll need working versions of all of Python 3.9
through 3.13 installed and on `PATH` as `python3.9`, `python3.10`, etc. The
nonlocal test suite is run for each `tox` environment, so it's best to use at
most two parallel sub-processes to avoid oversaturating your network bandwidth;
e.g.:

```bash
$ tox -rp2
```

## Code Autoformatting

The project is set up with a `tox` environment to blacken the codebase; run with:

```bash
$ tox -e black
```


## Linting

The project uses a number of lints, which are checked using
[`flake8`](https://flake8.pycqa.org/en/latest/) in CI. To run the lints locally,
it's easiest to use `tox`:

```bash
$ tox -e flake8
```

In some limited circumstances, it may be necessary to add
[`# noqa`](https://flake8.pycqa.org/en/stable/user/violations.html#in-line-ignoring-errors)
or
[`per_file_ignores`](https://flake8.pycqa.org/en/stable/user/options.html#cmdoption-flake8-per-file-ignores)
exclusions to the `flake8` lints. Please note these for discussion in an
issue/PR comment as soon as you think they might be needed.

Additionally, the CI for pull requests is set up to check that all modules,
functions, classes and methods have docstrings using the
[`interrogate`](https://pypi.org/project/interrogate/) package. There's a `tox`
environment for running this check, also:

```bash
$ tox -e interrogate
```


## Type Hints

I'd like to [roll out typing](https://github.com/bskinn/sphobjinv/issues/132) on
the project at some point in the future, and add
[`mypy`](https://github.com/python/mypy) checking to CI. A top-to-bottom effort
to add types doesn't make sense at the moment, though, given open issues like
[#118] and [#290]. So, for now, types on contributed code are welcomed, but optional.
Once the codebase is typed, though, they will be a required part of any PR
touching code.


## Documentation

All of the project documentation except the README is generated via
[Sphinx](https://github.com/sphinx-doc/sphinx). API changes must be documented
in the relevant docstring(s), and possibly also in the prose portions of the
documentation. Please use the modified
[NumPy-style](https://numpydoc.readthedocs.io/en/latest/format.html) formatting
for docstrings that is already in use in the project. Other changes may also
warrant documentation changes.

A large number of reStructuredText substitutions are defined in the `rst_epilog`
setting within `conf.py`, to make the documentation source more readable. Feel
free to add more entries there.

To run any of the Sphinx builders, first change to the `/doc` directory in the
repository tree. In most cases, a plain `make html` invocation is sufficient to
build the docs properly, as Sphinx does its best to detect which files were
changed and rebuild only the minimum portion of the documentation necessary. If
the docs seem not to be rendering correctly, try a clean build:

```bash
# Linux/Mac
doc $ make clean html

# Windows
doc> make -Ea
```

It's also a good idea to build the complete docs every once in a while with the
['nitpicky' option](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-nitpicky),
in order to detect any broken cross-references, as these will fail the
[Azure CI pipeline](#continuous-integration):

```bash
# Linux/Mac
doc $ O=-n make clean html

# Windows
doc> make html -Ean
```

You can also run the doctests with `make doctest` and the link validity checker
with `make linkcheck`.


## Continuous Integration

Both Github Actions and Azure Pipelines are set up for the project, and should
run on any forks of the repository.

Github Actions runs the test suite on Linux for Python 3.9 through 3.13, as well
as the `flake8` lints and the Sphinx doctests. By default, the Github Actions
will run on all commits, but the workflows can be skipped per-commit by
including `[skip ci]` in the commit message.

The Azure Pipelines CI runs an extensive matrix of cross-platform and
cross-Python-version tests, as well as numerous other checks. Due to its length,
it is configured to run only on release branches and PRs to `main` or `stable`.
The Azure Pipelines workflows now [also obey `[skip ci]`
directives](https://learn.microsoft.com/en-us/azure/devops/pipelines/repos/azure-repos-git?view=azure-devops&tabs=yaml#skipping-ci-for-individual-pushes).


## CHANGELOG

The project
[`CHANGELOG`](https://github.com/bskinn/sphobjinv/blob/main/CHANGELOG.md) should
be updated for the majority of contributions. No tooling is in place (e.g.,
[`towncrier`](https://github.com/twisted/towncrier)) for automated collation of
news items into `CHANGELOG`; all changes should be documented manually, directly
in the `CHANGELOG`. Please follow the format currently in use.

Any PR that touches the project code *must* include a `CHANGELOG` entry.
Contributions that make changes just to the test suite should usually also
include a `CHANGELOG` entry, except for very minor or cosmetic changes. Other
changes of note (packaging/build tooling, test/lint tooling/plugins, tool
settings, etc.) may also warrant a `CHANGELOG` bullet, depending on the
situation. When in doubt, ask!


## Issue and PR Templates

I've set up the project with a PR template and a couple of issue templates, to
hopefully make it easier to provide all the information needed to act on code
contributions, bug reports, and feature requests. If the templates don't fit the
issue/PR you want to create, though, then don't use them.


## License

All code and documentation contributions will respectively take on the MIT
License and CC BY 4.0 license of the project at large.


[#118]: https://github.com/bskinn/sphobjinv/issues/118
[#290]: https://github.com/bskinn/sphobjinv/issues/290
