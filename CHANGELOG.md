## CHANGELOG: sphobjinv -- Sphinx objects.inv Inspection/Manipulation Tool

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project follows an extension of
[Semantic Versioning](http://semver.org/spec/v2.0.0.html), where a bump in a
fourth number represents an administrative maintenance release with no code
changes.

### *Unreleased*

...


### [2.3.1.3] - 2025-05-26

#### Tests

  * Add `pytest-retry` to dev requirements and some `flaky` marks ([#306]).
    * Hopefully will iron out some of the test failures due to transient network
      problems.
  * Skip more characters in `test_name_lead_chars` for Sphinx 8.2+, that started
    using `splitlines()` instead of `split('\n')` ([#315]).
    * Add the boundary Sphinx versions 8.1.3 and 8.2.0 to the tox env list.

#### Internal

  * Remove job to post a notice on new PRs ([#316]).
    * The permissions aren't such that it works on PRs from forks, so there's no
      reason to have it run.
  * Remove Codecov ([#316]).
    * It's over-weight for a project and team of this size, and is not worth
      trying to make work in its current incarnation.
  * Remove `--nonloc` from CI Python/OS test matrix jobs and add new, targeted
    `--nonloc` job ([#316]).
    * Having this many jobs pulling this many inventories at once from remote
      sites has started to trigger `429 Too Many Requests` responses. Best to
      lighten the testing load.
  * Coalesce all CI into GitHub Actions, re-organize, and add tailored execution
    contexts ([#306]).
    * Contexts:
      * DRAFT PRs: Tests run on Python 3.12 for Windows and Linux
       READY PRs:
        * Full Mac/Win/Linux test matrix on Python 3.9-3.11, 3.13 (GIL)
        * Doctests
        * Linting
      * READY RELEASE PRs:
        * sdist builds and is testable
        * Docs build with warnings treated as errors
        * flake8 noqa check (nofail, info only)
        * Doctests on README Python
        * Coverage check for test suite code
      * OPENED, READY PRs: Post a comment on the PR noting that CI is much
        lighter for draft PRs.
    * Delete Azure Pipelines and old GitHub Actions config

  * Remove obsolete `pep517` from requirements ([#306]).

  * Rename `flake8-noqa` tox environment to `flake8_noqa` ([#306]).
    * `-` has special meaning when naming tox envs/deps, best to avoid it.

  * Bump dev Sphinx version to 7.4.7 ([#305]).
    * We stay under 8.0 because Sphinx v8 drops Python 3.9.

  * Clean up dependencies ([#305]).
    * Remove `pytest-ordering`, as it is no longer used in the test suite and is
      falling out of maintenance enough to start causing some things to fail.
    * Remove `sphinx-removed-in`, as `.. versionremoved::` is now a Sphinx
      built-in.
    * Remove `interrogate`, `pre-commit`, `rope`, `wget` from `requirements-dev.txt`.
      * No longer used for most; for `rope`, now no plans to use it.


### [2.3.1.2] - 2024-12-22

#### Internal

  * **DOC RENDERING FIX**: The `super` keyword used in a statement in the HTML footer
    template was missing parentheses to perform a method call; this
    caused the template rendering to emit a Python string describing
    the parent template object, instead of rendering the parent
    template as intended.
    ([#298](https://github.com/bskinn/sphobjinv/issues/298))

  * Moved the Sphinx linkcheck job out of CI and into `tox`.
    * The linkcheck is often flaky, and is a nuisance when it fails the CI. For
      uncertain reasons, the flakiness has increased noticeably in recent
      months. Less-frequent link checking, at release-time, is sufficient; so,
      we move the check out of CI.

  * Renamed `.readthedocs.yml` to `.readthedocs.yaml` to comply with the new,
    strict RtD requirement.

  * Added read-only GitHub PAT to Azure Pipelines config to ensure Python 3.13
    retrieval from GitHub doesn't hit a rate limit.

  * Update flake8 version pin in `requirements-flake8.txt` to avoid a bug in
    `pycodestyle`.

  * Removed `.pre-commit-config.yaml`, to remove the expectation of using
    pre-commit from the project.
    * For a project with this low an external contribution volume, the costs
      outweigh the benefits.

  * Added a `black` environment to `tox` for convenience and better
    encapsulation.

  * Added `flake8-black` to `requirements-flake8.txt` so that blackened status
    is checked as part of the linting, whether run manually or in CI.

#### Administrative

  * Added support for Python 3.13.

  * Dropped support for Python 3.8 (EOL).

  * Revised and updated `CONTRIBUTING.md`.

  * Updated link target of Pepy badge to match the new URL format.

  * Bumped Read the Docs Python version to 3.12.


### [2.3.1.1] - 2024-05-21

#### Tests

  * Update test machinery for the shell examples in the README, downstream of
    the conversion to Markdown ([#289]).

#### Administrative

  * Added formal support for Python 3.12.

  * Removed formal support for Python 3.7, which is end-of-life.

  * Bump `checkout` and `setup-python` GitHub Actions versions ([#289]).

  * Convert README from reST to Markdown ([#289], fixes [#287]).

  * Fix some broken/redirecting docs links ([#289]).

  * Adjust `flake8` configuration to account for some new lint warnings/errors
    ([#289]).


### [2.3.1] - 2022-11-29

#### Changed

  * The printout of the inferred `intersphinx_mapping` item for inventories
    retrieved by URL (`--url`) in the 'suggest' CLI mode is now relocated to
    fall immediately below the inventory-search output. It also now is displayed
    even if no objects in the `objects.inv` satisfy the score threshold.
    ([#262](https://github.com/bskinn/sphobjinv/issues/262))

  * The 'suggest' CLI mode output now includes dividers for improved
    readability.

#### Tests

  * The plaintext `tests/resource/objects_attrs.txt` was converted to POSIX EOLs
    and declared as binary to git, in order to provide a consistent state for
    sdist packaging, regardless of platform (POSIX vs Windows).

    * As a result, it was necessary to modify the `scratch_path` fixture to
      "`unix2dos`" this file on Windows systems, in order to provide a
      consistent test state.

    * Similarly, the `decomp_cmp_test` fixture was modified to "`unix2dos`" the
      `objects_attrs.txt` resource before comparisons, again in order to provide
      a consistent reference artifact. Implementing required direct manipulation
      of the bytes contents of the file, instead of the `filecmp.cmp` method
      that had been used previously.

  * The README doctests and shell tests have been removed from the default
    pytest suite. They must be explicitly opted-in with the `--readme` and
    `--doctest-glob="README.rst"` flags to pytest.

    * A new job, `readme`, has been added to the `aux_tests` stage of the Azure
      Pipelines CI to run these tests for PRs and release branches.

  * The constraint for `pytest-check` was bumped to `>=1.1.2` and all uses of
    the `check` fixture were revised from `with check.check(...):` to
    `with check(...):`. ([#265](https://github.com/bskinn/sphobjinv/issues/265))

  * Azure Pipelines now has Python 3.11 available for all of Ubuntu, Windows and
    MacOS, so it was added to the core text matrix for all platforms.

  * A new CI job was created on Azure Pipelines that creates an sdist from the
    current project, extracts it into a sandboxed environment, installs the dev
    dependencies, and runs the pytest suite (`azure-sdisttest.yml`).

  * All uses of `pytest-check` were updated to use the
    [v1.1.2 syntax](https://github.com/okken/pytest-check/blob/main/changelog.md#110---2022-nov-21)
    (`check` fixture, or `from pytest_check import check`).

#### Internal

  * The `sys.exit()` in the case of no objects falling above the 'suggest'
    search threshold was refactored into the main `do_suggest()` body, to
    minimize the surprise of an `exit()` call coming in a subfunction.
    ([#263](https://github.com/bskinn/sphobjinv/issues/263))

#### Packaging

  * `MANIFEST.in` was revised in order to provide a testable (`pytest --nonloc`)
    sdist, in order to streamline packaging of `sphobjinv` for conda-forge.
    (Thanks very much to [@anjos](https://github.com/anjos) for getting the
    recipes for `sphobjinv` and its dependencies in place! See
    [#264](https://github.com/bskinn/sphobjinv/issues/264).)

#### Administrative

  * `sphobjinv` is now available via conda-forge! A note was added to the docs
    to indicate this.

  * The version bump on `pytest-check` no longer permits the use of Python 3.6
    in CI. As Python 3.6 is nearly a year beyond EOL, this seems a reasonable
    time to officially drop support for it. `python_requires` will still be at
    `>=3.6` for now; it *should* still work for 3.6...but, no guarantees.

  * The hook versions for `pre-commit-hooks`, `black`, and `pyproject-fmt` were
    updated to v4.3, v22.10, and v0.3.5, respectively.

  * `CONTENT_LICENSE.txt` was created, to specifically house the full
    content/documentation license information.

  * `LICENSE.txt` was revised to only hold the MIT License for the code,
    primarily so that Github's automatic systems will recognize the project as
    MIT licensed.

  * Caching of pip downloads was added to all of the Azure Pipelines jobs.

  * The version constraint for `pytest-check` was raised to `>=1.1.2`.

  * A temporary upper bound was placed on the `flake8` version (now `>=5,<6`,
    instead of `>=5`) to avoid pip resolver failures likely due to conflicts
    with constraints declared by plugins.

  * The older versions of `jsonschema` tested in the `tox` matrix were
    streamlined down to 3.0 (`==3.0`), 3.x (`<4`), 4.0 (`<4.1`) and 4.8
    (`<4.9`).

  * The pin of `sphinx-issues==0.4.0` in the `tox` matrix was removed, to match
    the unpinned package in the `requirements-xxx.txt` files.


### [2.3] - 2022-11-08

#### Added

  * The CLI now prints the project name and version for the `objects.inv` as
    part of the 'suggest' mode output.

  * The CLI now prints an inferred `intersphinx_mapping` entry for a remote
    docset as part of the 'suggest' mode output, where such inference is
    possible. The output from this mapping inference was added to the relevant
    tests, and a couple of unit tests on some basic pieces of functionality were
    written. ([#149](https://github.com/bskinn/sphobjinv/issues/149))

  * The CLI now provides considerably more information about what is happening
    with the URLs it checks when trying to retrieve a remote inventory.
    ([#99](https://github.com/bskinn/sphobjinv/issues/99), plus more)

  * CLI 'suggest' results output now displays more information about
    the total number of objects in the inventory, the search score threshold,
    and the number of results falling at/above that threshold.
    ([#232](https://github.com/bskinn/sphobjinv/issues/232))

  * A new CLI option, `-p`/`--paginate`, enables paging of the results from the
    `suggest` feature. ([#70](https://github.com/bskinn/sphobjinv/issues/70))

#### Fixed

  * The regex for parsing object lines from decompressed inventories now
    correctly processes `{role}` values that contain internal colons.

  * CLI corner case where options are passed but no subparser is specified
    now results in a clean error-exit, instead of an exception.
    ([#239](https://github.com/bskinn/sphobjinv/issues/239))

#### Documentation

  * Updated doctests to reflect the new v22.1 attrs `objects.inv` used for
    demonstration purposes.

  * Updated `syntax.rst` to indicate that the `{role}` in an inventory object
    MAY contain a colon.

  * Added new 'CLI implementation' pages for the new modules, downstream of the
    refactoring of the CLI 'convert' and 'suggest' code.

  * Revised the intro paragraph of the 'CLI usage' page to more clearly emphasize
    the two CLI subcommands and the links to their respective docs pages.

  * Fixed a mistake in the CLI help info for the `--url` argument to `convert`.

#### Tests

  * Various tests were updated to reflect the contents of the new v22.1 attrs
    `objects.inv` introduced to replace the previous v17.2 inventory.

  * A modern Sphinx `objects.inv` (v6.0.0b) was added to `tests/resource` as
    `objects_sphinx.inv`, and the previous v1.6.6 was renamed to
    `objects_sphinx_1_6_6.inv`.

  * The 'valid objects' test cases were updated to reflect the possibility for a
    colon within `{role}`:

    * The colon-within-`{role}` test case was moved from 'invalid' to 'valid'.

    * The colon-within-`{domain}` test case was also moved from 'invalid' to
      'valid', but with an annotation added to indicate that it's not actually
      viable---it will actually be interpreted incorrectly, with the first
      portion of the colon-containing `{domain}` imported as `{domain}`, and the
      remainder imported as part of `{role}`.

#### Internal

  * Refactor CLI code to place the 'convert' and 'suggest' implementations in
    their own modules.

  * Refactor CLI 'suggest' code to the main `do_suggest()` function and a
    handful of sub-functions.

  * Rename the `log_print()` CLI helper function to the more-descriptive
    `print_stderr()`.

  * Bump development Sphinx version to v5.3.

  * Bump flake8 version to >=5, due to the absorption of flake8-colors
    colorization functionality. The flake8/tox config was updated accordingly.

  * Bump pre-commit black hook to v22.3.0.

  * Remove PyPy and Python 3.6 from Azure Pipelines test matrix.

  * Revise `__version__` retrieval in `setup.py` to use an intermediate
    dictionary with `exec()`.

  * Update `setup.cfg` to use `license_files`, instead of the deprecated
    `license_file`.

#### Administrative

  * Apply CC BY 4.0 to documentation and docstrings and update project files to
    reflect.


### [2.2.2] - 2022-03-22

#### Fixed

  * UnicodeDecodeErrors are ignored within the vendored `fuzzywuzzy` package
    during `suggest` operations, using the `errors=replace` mode within
    bytes.decode().

    * This misbehavior emerged after vendoring `fuzzywuzzy`, suggesting that
      it was a bug fixed later on in that project's development, after the
      point from which it was vendored.

    * This change may alter `suggest` behavior for those inventory objects with
      pathological characters. But, given their rarity, user experience is not
      expected to be noticeably affected.

#### Internal

  * The `pyproject-fmt` formatted was added as a pre-commit hook.

  * The `flake8-raise` plugin was added to the linting suite.

#### Testing

  * A smoke test for error-free `suggest` execution was added for all of the
    inventory files in `tests/resource`.


### [2.2.1] - 2022-02-05

#### Internal

  * The `benchmarks.py` file within the vendored version of `fuzzywuzzy`
    was removed. This *should* have no effect on `sphobjinv` functionality.
    * Per [#223](https://github.com/bskinn/sphobjinv/issues/223), the
      Python 2 code within `benchmarks.py` breaks a full-source compilation
      done as part of an RPM packaging workflow.


### [2.2] - 2022-01-30

#### Administrative

  * The project documentation has been updated to reflect the deprecation
    of the `python-Levenshtein` speedup.

  * `pre-commit` has been added to the project, primarily to automate
    `black` code formatting on every commit.

    * The default trailing-whitespace, end-of-file, YAML syntax, and
      large-file-prevention hooks have also been added.

#### Internal

  * `sphinx-removed-in` was added as a dev and RTD dependency, to provide
    the `versionremoved` Sphinx directive.


### [2.2b1] - 2021-12-23

#### Removed

  * Acceleration of the `suggest` functionality via use of `python-Levenshtein`
    is no longer possible due to the vendoring of an early, MIT-licensed version
    of `fuzzywuzzy`, as noted below. The `speedup` install extra is now obsolete,
    and has been removed.

#### Internal

  * The `fuzzywuzzy` string matcher was vendored into the project from a point
    in its development history before the `python-Levenshtein` dependency,
    and its corresponding GPL encumbrance, was introduced.

#### Administrative

  * Project default branch migrated to `main` from `master`.

  * Standard development Python version bumped to 3.10.

  * Standard development Sphinx version bumped to 4.3.1.

  * Active support for Python 3.11 added.


### [2.1] - 2021-04-14

#### Added

  * Python 3.10 support was officially added.

#### Changed

  * The User-Agent header sent by `Inventory` when making an HTTP(S) request
    now identifies `sphobjinv` and its version (anticipate no API or
    behavior change).

  * An extraneous newline was removed before tables printed in the
    'suggest' CLI mode (cosmetic change).

#### Fixed

  * Previously, `sphobjinv.Inventory` would ignore entries in `objects.inv`
    that contained spaces within `name`
    (see [#181](https://github.com/bskinn/sphobjinv/issues/181));
    this is now fixed.

#### Removed

  * Python 3.5 is no longer supported.

  * The relaxation of the integer constraint on the `priority` field
    introduced in v2.1b1 has been *reverted*, as `objects.inv` data lines
    with such non-integer `priority` values are skipped by Sphinx.

#### Internal

  * Where possible, string interpolation has been refactored to use
    f-strings.

  * A 'speedup' `extras_require` entry has been added to allow simple installation
    of `python-Levenshtein` for Linux and MacOS platforms, as
    `pip install sphobjinv[speedup]`. This extra does nothing on Windows, since
    compilation machinery is anticipated not to be available for most users.

  * `objects_mkdoc_zlib0.inv`, which was compressed at `zlib` level 0,
    has been added to the test resources directory.

  * This file had to be flagged as binary in `.gitattributes` in order to avoid
      git EOL auto-conversion on Windows.

  * The CLI functionality was refactored from the single `sphobjinv.cmdline` module
    into a dedicated set of `sphobjinv.cli.*` submodules.

  * Some internal `type(...) is ...` checks were replaced with `isinstance(...)`

#### Testing

  * Added *significant* body of new tests to confirm inventory compatibility
    with both `sphobjinv` and Sphinx itself.

    * Consistency checks added both for data within `sphobjinv.Inventory` instances
      **AND** as emitted from `sphinx.ext.inventory.InventoryFile.load()`.

    * The tests in `tests/test_valid_objects.py` strive to bracket as precisely
      as possible what content is allowed on an `objects.inv` data line,
      in addition to providing guidance on what is allowable, but discouraged.

      `docs/source/syntax.rst` was also edited to reflect this guidance.

  * Additional tests have been added to probe corner cases involving Windows EOLs.

  * A test was added to ensure that the schema in `sphobjinv.schema` is in fact
    a valid JSON schema.

  * Multiple asserts/checks per test method have been converted to use
    `pytest-check` instead of `pytest-subtests`, due to some inconsistent
    behavior with the latter.

  * `tox` environments and dependencies were updated, and some flake8 configuration
    was adjusted.

#### Administrative

  * Standard development Python version bumped to 3.9.

  * Standard development Sphinx version bumped to 3.5.0.

  * Added `[skip ci]` flag in commit text for skipping Github Actions CI.

  * RtD upgraded to use Python 3.8.

  * Added 'radio Sphinx' logo to RtD docs.

  * Drafted `CONTRIBUTING.md` and added PR & issue templates.

  * Tranferred most project metadata from `setup.py` to `setup.cfg`.


### [2.1b1] - 2020-11-13

#### Fixed

  * Equality tests on Inventory and DataObjStr/DataObjBytes instances
    now work correctly.

  * Non-integer and non-numeric values for `priority` are now accepted
    during `Inventory` instantiation, consistent with what is allowed
    by `DataObjStr` and `DataObjBytes` instantiation.


### [2.1a2] - 2020-10-27

#### Added

  * When an inventory is retrieved via CLI from a remote URL with `-u`,
    the resolved location of the inventory is included in generated JSON
    at `json_dict.metadata.url`.

#### Changed

  * CLI logging messages are now emitted to stderr instead of stdout.


### [2.1a1] - 2020-10-26

#### Added

  * A hyphen can now be passed as the CLI input and/or output file name
    to instruct sphobjinv to use stdin and/or stdout, respectively.

  * The `fileops` and `inventory` APIs are now tested to work with
    both strings and `pathlib.Path` objects, where they interact
    with the filesystem.

#### Refactored

  * Patterns in regular expressions are now defined with raw strings
    to improve readability.


### [2.0.1] - 2020-01-26

#### Fixed

  * attr.s usage on Inventory changed to use eq=False where possible,
    per the deprecation of the cmp argument.

  * URL inventory retrieval now sends a User-Agent header, to avoid
    403 FORBIDDEN errors on some docs servers.


### [2.0.1rc1] - 2019-02-01

#### Fixed

  * Sphinx *can* generate inventories with empty-string values for
    `project` and `version`; `sphobjinv` now can import such
    inventories without error.


### [2.0.0] - 2018-08-16

#### Added

  * Loading remote inventories from the CLI now will
    perform an automatic walk along the directory structure of the
    provided URL, searching for the objects.inv file of the
    documentation set.
  * The above URL walking functionality is exposed for API use
    at sphobjinv.fileops.urlwalk.

#### Changed

  * Instances of DataObjStr and DataObjBytes are NO LONGER IMMUTABLE.
    Working with Inventory instances was going to be far too cumbersome
    with immutable DataObjStr instances in .objects.


### [2.0.0rc1] - 2018-05-18

#### Fixed

  * API code no longer contains any `sys.exit` calls;
    CLI interactions should now be properly segregated from the internal API.

#### Added

  * API
    * Data for individual objects encapsulated in the new `.data.DataObjStr` and
    * `.data.DataObjBytes` classes
    * Instances of these objects provide granular access to the contained data
    * Instances are *immutable*, but expose an `evolve()` method for creating new,
      (optionally) modified instances.
   * Entire inventory contents, as a `list` of `DataObjStr`, encapsulated in
     `.inventory.Inventory` instances
     * `Inventory` instances are anticipated to be the primary point of user interface to
       inventory data
     * `.suggest()` method added, exploiting fuzzy string searching by
       [`fuzzywuzzy`](https://pypi.org/project/fuzzywuzzy) for rapid searching of
       inventories for objects of interest
     * Import of remote `objects.inv` files via `urllib.request` and `certifi` implemented.
   * Helper methods are provided for working with the `objects.inv` shorthands for object
     URI and display-name information, on both `DataObj...` and `Inventory` instances.
   * `readjson`/`writejson` helper functions added to `.fileops`
   * JSON schema added to `.schema` for use with
     [`jsonschema`](https://pypi.org/project/jsonschema) to validate incoming data
     during `Inventory` instantiation from  JSON
 * Command-line interface
   * Add `suggest` subparser, for recommendation of matching objects
     within an input inventory
   * Add ability to read and write JSON inventories
   * Add ability to use a remote `objects.inv` file (arbitrary filename) as input,
     specified by URL
   * Add arguments to:
     * Expand/contract the `objects.inv` URI and 'display name' abbreviations
     * Force overwrite of an existing output file without prompting
     * Silence all output (mainly intended for scripting applications);
       includes automatic overwriting of an existing output file
     * Various arguments to control the output of a `sphobjinv suggest` invocation

#### Changed

 * `readfile`/`writefile` changed to `readbytes`/`writebytes`
   and moved to new `.fileops` submodule
 * `decode`/`encode` changed to `decompress`/`compress` and moved to new `.zlib` submodule
 * `p_data`/`p_comments` regex patterns renamed with `pb_` prefix to indicate they are
   `bytes`, not `str` patterns
 * CLI
   * Commands for (de)compressing `objects.inv` files changed to a more general `convert`
     subparser, due to addition of JSON output option
   * Default filename/extension assumptions removed from input file argument,
     as multiple input formats make the logic here complicated enough
     it's not worth messing with

### [1.0.0] - 2016-05-24

#### Features

 * Flexible commandline encode and decode of objects.inv
   files, in terms of file names and input/output locations
 * Programmatic conversion via API is available, but
   potentially buggy due to poor segregation of cmdline
   behaviors. This is to be fixed.


[#287]: https://github.com/bskinn/sphobjinv/issues/287
[#289]: https://github.com/bskinn/sphobjinv/pull/289
[#305]: https://github.com/bskinn/sphobjinv/pull/305
[#306]: https://github.com/bskinn/sphobjinv/pull/306
[#315]: https://github.com/bskinn/sphobjinv/pull/315
[#316]: https://github.com/bskinn/sphobjinv/pull/316
