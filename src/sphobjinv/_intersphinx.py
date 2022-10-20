r"""``intersphinx`` *helpers for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

This module is PRIVATE. The API details here may change without
warning. If you would like to be able to rely on these functions,
please open an issue describing your use-case:
https://github.com/bskinn/sphobjinv/issues

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    12 Jun 2022

**Copyright**
    \(c) Brian Skinn 2016-2022

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

from urllib import parse as urlparse

from sphobjinv.error import SOIIsphxNoMatchingObjectError, SOIIsphxURINotASuffixError


def _strip_url_to_netloc_path(url, *, with_scheme=False):
    """Reduce a URL to only netloc and path, optionally with scheme."""
    parts = urlparse.urlsplit(url)
    trimmed = parts._replace(
        query="",
        fragment="",
    )

    if not with_scheme:
        trimmed = trimmed._replace(scheme="")

    return urlparse.urlunsplit(trimmed)


def extract_objectsinv_url_base(objectsinv_url):
    """Infer a base URL for the provided ``objects.inv`` inventory URL.

    If this function is a no-op, then the resulting base is NOT RELIABLE,
    because the URL did not end with ``/objects.inv``.

    If this function *does* make a change, then the resulting base is
    RELATIVELY RELIABLE, since the only change that should occur is
    stripping of a ``/objects.inv`` suffix, which strongly implies but
    does not guarantee that the URL came from a Sphinx docset in the
    standard multi-page HTML layout.

    Parameters
    ----------
    objectsinv_url

        |str| -- URL from which to attempt docset base inference

    Returns
    -------
    trimmed

        |str| -- URL after attempt to trim a trailing ``/objects.inv``

    """
    trimmed = _strip_url_to_netloc_path(objectsinv_url, with_scheme=True)
    return f"{trimmed.rpartition('/objects.inv')[0]}/"


def _is_url_path_suffix(ref_url, suffix_candidate):
    """Indicate whether the candidate path is a suffix of the reference URL."""
    # We want any fragments/queries/parameters to be stripped off of BOTH
    # the ref_url and the suffix_candidate.
    # The scheme of the ref_url doesn't matter since we're only inspecting
    # the end of the URL.
    return _strip_url_to_netloc_path(ref_url).endswith(
        _strip_url_to_netloc_path(suffix_candidate)
    )


def _find_obj_with_matching_uri(ref_url, inv):
    """Provide an object from the inventory whose URI is a suffix of the reference URL.

    Returns ``None`` if nothing found.

    """
    try:
        return next(
            o
            for o in inv.objects
            if o.uri  # Must not be empty string
            and not o.uri.startswith("#")  # Must not only be a fragment
            and _is_url_path_suffix(ref_url, o.uri)  # Must be a suffix of the ref URL
        )
    except StopIteration:
        return None


def _extract_base_from_weburl_and_uri(web_url, uri):
    """Extract the base URL from a reference web URL and the given URI.

    The base URL is returned **with** a trailing forward slash.

    Raises sphobjinv.error.SOIIsphxNotASuffixError if trimmed ``uri`` is
    not actually a suffix of ``web_url``.

    """
    if not _is_url_path_suffix(web_url, uri):
        raise SOIIsphxURINotASuffixError(web_url=web_url, uri=uri)

    trimmed = _strip_url_to_netloc_path(web_url, with_scheme=True)

    # TODO: Once the project drops Python < 3.9, can reimplement with .removesuffix()
    return trimmed[: trimmed.find(_strip_url_to_netloc_path(uri))]


def _extract_base_from_weburl_and_inventory(web_url, inv):
    """Extract a candidate base URL from a docset web URL and an Inventory instance."""
    obj = _find_obj_with_matching_uri(web_url, inv)

    if obj is None:
        raise SOIIsphxNoMatchingObjectError(web_url=web_url, inv=inv)

    return _extract_base_from_weburl_and_uri(web_url, obj.uri)


def infer_mapping(web_url, objectsinv_url, inv):
    """Infer a best-guess intersphinx_mapping entry for the given URLs and Inventory.

    Parameters
    ----------
    web_url

        str -- URL of a valid page (optionally with fragment) from a live docset

    objectsinv_url

        str -- URL of the ``objects.inv`` file for the live docset

    inv

        |Inventory| -- Instantiated inventory for the live docset---MAY be generated
        from the ``objects.inv`` at `objectsinv_url`, but CAN be generated from
        any ``objects.inv`` corresponding to the **same version** of the live docset


    Returns
    -------
    mapping

        (str, str or None) -- Inferred ``intersphinx_mapping`` entry


    """
    objectsinv_base = extract_objectsinv_url_base(objectsinv_url)
    weburl_base = _extract_base_from_weburl_and_inventory(web_url, inv)

    return (weburl_base, None if objectsinv_base == weburl_base else objectsinv_url)
