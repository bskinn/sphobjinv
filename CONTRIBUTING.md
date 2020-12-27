Introduction

- Drop a line on Twitter @btskinn with questions,
  or open an issue


Setting up the project

- Clone
- Virtual environment
- Install req'ts-dev
- Build docs (needed for some tests)

Tests

- pytest
- Defaults to only running tests not using network (local);
  do pytest --nonloc to test also  nonlocal things
- tox is set up not to be the everyday test runner,
  but instead to execute a detailed check of compatibility
  of Python and package dependency versions
- Maintain 100% test coverage in any PRs
  (discuss before using any pragma no cover)

Linting

- Bunch of stuff in flake8 (tox -e flake8)
- Docstring existence check via interrogate
  (tox -e interrogate)
- Discuss before using any noqa or exclusions


Continuous Integration

- GHA for basic test runs on Linux, all commits
- AP for extensive testing, only on PRs to master/stable
  and on release branches


Documentation

- Docstrings---numpy style
- Add/change for functionality changes
- make clean html for POSIX/Mac
- make html -Ean for Windows
- make doctest
- make linkcheck


Type Hints

- Future issue is adding types across the project
  (would be a great contribution?)

CHANGELOG

- Anything that touches code or tests definitely
  needs a CHANGELOG bullet
- Other changes of note (packaging, building, testing/linting
  tooling, tool settings, etc.) may warrant a CHANGELOG bullet;
  depends

Using issue/PR templates

- For most bug reports and feature requests,
  should use
- Use judgment, though -- if the templates don't
  really fit, don't worry about using them.

