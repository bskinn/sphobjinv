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
    """Provide the base URL for the provided objects.inv inventory URL."""
    trimmed = _strip_url_to_netloc_path(objectsinv_url, with_scheme=True)
    return f"{trimmed.rpartition('/')[0]}/"


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


def _url_matchup(web_url, objectsinv_url, inv):
    objectsinv_base = _extract_objectsinv_url_base(objectsinv_url)
    return objectsinv_base == _extract_base_from_weburl_and_inventory(web_url, inv)
