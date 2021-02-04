r"""Module for ``sphobjinv`` *CLI |Inventory| loading*.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    17 Nov 2020

**Copyright**
    \(c) Brian Skinn 2016-2021

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import json
import sys
from json import JSONDecodeError
from urllib.error import HTTPError, URLError

from jsonschema.exceptions import ValidationError

from sphobjinv import Inventory, readjson, urlwalk, VersionError
from sphobjinv.cli.parser import PrsConst
from sphobjinv.cli.paths import resolve_inpath
from sphobjinv.cli.ui import err_format, log_print


def import_infile(in_path):
    """Attempt import of indicated file.

    Convenience function wrapping attempts to load an
    |Inventory| from a local path.

    Parameters
    ----------
    in_path

        |str| -- Path to input file

    Returns
    -------
    inv

        |Inventory| or |None| -- If instantiation with the file at
        `in_path` succeeds, the resulting |Inventory| instance;
        otherwise, |None|

    """
    # Try general import, for zlib or plaintext files
    try:
        inv = Inventory(in_path)
    except AttributeError:
        pass  # Punt to JSON attempt
    else:
        return inv

    # Maybe it's JSON
    try:
        inv = Inventory(readjson(in_path))
    except JSONDecodeError:
        return None
    else:
        return inv


def inv_local(params):
    """Create |Inventory| from local source.

    Uses |resolve_inpath| to sanity-check and/or convert
    |cli:INFILE|.

    Calls :func:`sys.exit` internally in error-exit situations.

    Parameters
    ----------
    params

        |dict| -- Parameters/values mapping from the active subparser

    Returns
    -------
    inv

        |Inventory| -- Object representation of the inventory
        at |cli:INFILE|

    in_path

        |str| -- Input file path as resolved/checked by
        |resolve_inpath|

    """
    # Resolve input file path
    try:
        in_path = resolve_inpath(params[PrsConst.INFILE])
    except Exception as e:
        log_print("\nError while parsing input file path:", params)
        log_print(err_format(e), params)
        sys.exit(1)

    # Attempt import
    inv = import_infile(in_path)
    if inv is None:
        log_print("\nError: Unrecognized file format", params)
        sys.exit(1)

    return inv, in_path


def inv_url(params):
    """Create |Inventory| from file downloaded from URL.

    Initially, treats |cli:INFILE| as a download URL to be passed to
    the `url` initialization argument
    of :class:`~sphobjinv.inventory.Inventory`.

    If an inventory is not found at that exact URL, progressively
    searches the directory tree of the URL for |objects.inv|.

    Injects the URL at which an inventory was found into `params`
    under the |cli:FOUND_URL| key.

    Calls :func:`sys.exit` internally in error-exit situations.

    Parameters
    ----------
    params

        |dict| -- Parameters/values mapping from the active subparser

    Returns
    -------
    inv

        |Inventory| -- Object representation of the inventory
        at |cli:INFILE|

    ret_path

        |str| -- URL from |cli:INFILE| used to construct `inv`.
        If URL is longer than 45 characters, the central portion is elided.

    """
    in_file = params[PrsConst.INFILE]

    # Disallow --url mode on local files
    if in_file.startswith("file:/"):
        log_print("\nError: URL mode on local file is invalid", params)
        sys.exit(1)

    # Need to initialize the inventory variable
    inv = None

    # Try URL as provided
    try:
        inv = Inventory(url=in_file)
    except (HTTPError, ValueError, VersionError, URLError):
        log_print("No inventory at provided URL.", params)
    else:
        log_print("Remote inventory found.", params)
        url = in_file

    # Keep searching if inv not found yet
    if not inv:
        for url in urlwalk(in_file):
            log_print(f'Attempting "{url}" ...', params)
            try:
                inv = Inventory(url=url)
            except (ValueError, HTTPError):
                pass
            else:
                log_print("Remote inventory found.", params)
                break

    # Cosmetic line break
    log_print(" ", params)

    # Success or no?
    if not inv:
        log_print("No inventory found!", params)
        sys.exit(1)

    params.update({PrsConst.FOUND_URL: url})
    if len(url) > 45:
        ret_path = url[:20] + "[...]" + url[-20:]
    else:  # pragma: no cover
        ret_path = url

    return inv, ret_path


def inv_stdin(params):
    """Create |Inventory| from contents of stdin.

    Due to stdin's encoding and formatting assumptions, only
    text-based inventory formats can be sanely parsed.

    Thus, only plaintext and JSON inventory formats can be
    used as inputs here.

    Parameters
    ----------
    params

        |dict| -- Parameters/values mapping from the active subparser

    Returns
    -------
    inv

        |Inventory| -- Object representation of the inventory
        provided at stdin

    """
    data = sys.stdin.read()

    try:
        return Inventory(dict_json=json.loads(data))
    except (JSONDecodeError, ValidationError):
        pass

    try:
        return Inventory(plaintext=data)
    except (AttributeError, UnicodeEncodeError, TypeError):
        pass

    log_print("Invalid plaintext or JSON inventory format.", params)
    sys.exit(1)
