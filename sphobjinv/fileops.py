r"""*File I/O helpers for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    5 Nov 2017

**Copyright**
    \(c) Brian Skinn 2016-2018

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    http://sphobjinv.readthedocs.io

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""


def readbytes(path):
    """Read file contents and return as |bytes|.

    Parameters
    ----------
    path

        |str| -- Path to file to be opened.

    Returns
    -------
    b

        |bytes| -- Contents of the indicated file.

    """
    with open(path, 'rb') as f:
        return f.read()


def writebytes(path, contents):
    """Write indicated file contents.

    Any existing file at `path` will be overwritten.

    Parameters
    ----------
    path

        |str| -- Path to file to be written.

    contents

        |bytes| -- Content to be written to file.

    """
    with open(path, 'wb') as f:
        f.write(contents)


def readjson(path):
    """Create |dict| from JSON file.

    No data or schema validation is performed.

    Parameters
    ----------
    path

        |str| -- Path to JSON file to be read.

    Returns
    -------
    d

        |dict| -- Deserialized JSON.

    """
    import json

    with open(path, 'r') as f:
        return json.load(f)


def writejson(path, d):
    """Create JSON file from |dict|.

    No data or schema validation is performed.
    Any existing file at `path` will be overwritten.

    Parameters
    ----------
    path

        |str| -- Path to output JSON file.

    d

        |dict| -- Data structure to serialize.

    """
    import json

    with open(path, 'w') as f:
        json.dump(d, f)


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
