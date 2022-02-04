## CHANGELOG: sphobjinv -- Sphinx objects.inv Inspection/Manipulation Tool

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project strives to adhere to
[Semantic Versioning](http://semver.org/spec/v2.0.0.html).


### [2.2.1] - 2022-02-03

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
