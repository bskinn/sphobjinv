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

from urllib.parse import urlsplit

from sphobjinv.error import SOIIsphxNotASuffixError


def _trim_url(url, *, with_scheme=False):
    parts = urlsplit(url)
    trimmed = f"{parts.netloc}{parts.path}"

    if with_scheme:
        trimmed = f"{parts.scheme}://" + trimmed

    return trimmed


def _is_url_path_suffix(ref, candidate):
    """Indicate whether the candidate path is a suffix of the ref."""
    return _trim_url(ref).endswith(_trim_url(candidate))


def _obj_with_matching_uri(ref, inv):
    """Provide an object in the invetory with a matching URI suffix.

    None if nothing found.

    """
    try:
        return next(o for o in inv.objects if _is_url_path_suffix(ref, o.uri))
    except StopIteration:
        return None


def _base_from_ref_and_suffix(ref, suffix):
    url = _trim_url(ref, with_scheme=True)

    if not url.endswith(suffix):
        raise SOIIsphxNotASuffixError(base=ref, suffix=suffix)

    # TODO: Once the project drops Python < 3.9, can reimplement with .removesuffix()
    return url[: url.find(suffix)]


def _base_from_ref_and_object(ref, obj):
    return _base_from_ref_and_suffix(ref, _trim_url(obj.uri))


def _base_from_ref_and_matching_object(ref, inv):
    work_obj = _obj_with_matching_uri(ref, inv)
    return _base_from_ref_and_object(ref, work_obj)


def _trim_object_uri(uri):
    return _trim_url(uri)


def _inventory_url_base(url):
    return f"{urlsplit(url).scheme}://{_trim_url(url).rpartition('/')[0]}/"


def _url_matchup(web_url, obj_url, inv):
    inventory_base = _inventory_url_base(obj_url)
    return inventory_base == _base_from_ref_and_matching_object(web_url, inv)
