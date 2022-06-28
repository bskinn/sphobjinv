r"""``intersphinx`` *helpers for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

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

from sphobjinv.error import SOIIsphxNoMatchingObjectError, SOIIsphxNotASuffixError


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


def _extract_objectsinv_url_base(objectsinv_url):
    """Provide the base URL for the provided objects.inv inventory URL.

    # TODO: Convert this to a public API function
    It should be useful as a fallback method of identifying a tentative
    mapping for a docset, given the way that the urlwalk generator
    steps through the possible objects.inv locations.

    If this function is a no-op, then the resulting base is NOT RELIABLE.
    If this function *does* make a change, then the resulting base is
    RELATIVELY RELIABLE.
    """
    trimmed = _strip_url_to_netloc_path(objectsinv_url, with_scheme=True)
    return f"{trimmed.rpartition('/objects.inv')[0]}/"


def _is_url_path_suffix(ref_url, suffix_candidate):
    """Indicate whether the candidate path is a suffix of the reference URL."""
    return _strip_url_to_netloc_path(ref_url).endswith(
        _strip_url_to_netloc_path(suffix_candidate)
    )


def _find_obj_with_matching_uri(ref_url, inv):
    """Provide an object from the inventory whose URI is a suffix of the reference URL.

    Returns None if nothing found.

    """
    try:
        return next(o for o in inv.objects if _is_url_path_suffix(ref_url, o.uri))
    except StopIteration:
        return None


def _extract_base_from_weburl_and_suffix(web_url, suffix):
    """Extract the base URL from a reference web URL and the given suffix.

    The base URL is returned **with** a trailing forward slash.

    Raises sphobjinv.error.SOIIsphxNotASuffixError if 'suffix' is
    not actually a suffix of ref_url.

    """
    trimmed = _strip_url_to_netloc_path(web_url, with_scheme=True)

    if not trimmed.endswith(suffix):
        raise SOIIsphxNotASuffixError(web_url=web_url, suffix=suffix)

    # TODO: Once the project drops Python < 3.9, can reimplement with .removesuffix()
    return trimmed[: trimmed.find(suffix)]


def _extract_base_from_weburl_and_inventory(web_url, inv):
    """Extract a candidate base URL from a docset web URL and an Inventory instance."""
    obj = _find_obj_with_matching_uri(web_url, inv)

    if obj is None:
        raise SOIIsphxNoMatchingObjectError(web_url=web_url, inv=inv)

    stripped_uri = _strip_url_to_netloc_path(obj.uri)

    return _extract_base_from_weburl_and_suffix(web_url, stripped_uri)


def infer_mapping(web_url, objectsinv_url, inv):
    """Infer a best-guess intersphinx_mapping entry for the given URLs and Inventory.

    # TODO: WRITE THIS DOCSTRING!
    """
    objectsinv_base = _extract_objectsinv_url_base(objectsinv_url)
    weburl_base = _extract_base_from_weburl_and_inventory(web_url, inv)

    return (weburl_base, None if objectsinv_base == weburl_base else objectsinv_url)
