r"""*File I/O helpers for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    5 Nov 2017

**Copyright**
    \(c) Brian Skinn 2016-2020

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""


def readbytes(path):
    """Read file contents and return as |bytes|.

    Parameters
    ----------
    path

        |str| or |Path| -- Path to file to be opened.

    Returns
    -------
    b

        |bytes| -- Contents of the indicated file.

    """
    with open(str(path), "rb") as f:
        return f.read()


def writebytes(path, contents):
    """Write indicated file contents.

    Any existing file at `path` will be overwritten.

    Parameters
    ----------
    path

        |str| or |Path| -- Path to file to be written.

    contents

        |bytes| -- Content to be written to file.

    """
    with open(str(path), "wb") as f:
        f.write(contents)


def readjson(path):
    """Create |dict| from JSON file.

    No data or schema validation is performed.

    Parameters
    ----------
    path

        |str| or |Path| -- Path to JSON file to be read.

    Returns
    -------
    d

        |dict| -- Deserialized JSON.

    """
    import json

    with open(str(path), "r") as f:
        return json.load(f)


def writejson(path, d):
    """Create JSON file from |dict|.

    No data or schema validation is performed.
    Any existing file at `path` will be overwritten.

    Parameters
    ----------
    path

        |str| or |Path| -- Path to output JSON file.

    d

        |dict| -- Data structure to serialize.

    """
    import json

    with open(str(path), "w") as f:
        json.dump(d, f)


def urlwalk(url):
    r"""Generate a series of candidate |objects.inv| URLs.

    URLs are based on the seed `url` passed in. Ensure that the
    path separator in `url` is the standard **forward** slash
    ('|cour|\ /\ |/cour|').

    Parameters
    ----------
    url

        |str| -- Seed URL defining directory structure to walk through.

    Yields
    ------
    inv_url

        |str| -- Candidate URL for |objects.inv| location.

    """
    # Scrub any anchor, as it fouls things
    url = url.partition("#")[0]

    urlparts = url.rstrip("/").split("/")

    # This loop condition results in the yielded values stopping at
    # 'http[s]://domain.com/objects.inv', since the URL protocol
    # specifier has two forward slashes
    while len(urlparts) >= 3:
        urlparts.append("objects.inv")
        yield "/".join(urlparts)
        urlparts.pop()
        urlparts.pop()
