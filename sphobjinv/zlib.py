# ----------------------------------------------------------------------------
# Name:        zlib
# Purpose:     zlib compression/decompression of content lines for sphobjinv
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     5 Nov 2017
# Copyright:   (c) Brian Skinn 2016-2018
# License:     The MIT License; see "LICENSE.txt" for full license terms
#                   and contributor agreement.
#
#       This file is part of Sphinx Objects.inv Encoder/Decoder, a toolkit for
#       encoding and decoding objects.inv files for use with intersphinx.
#
#       http://www.github.com/bskinn/sphobjinv
#
# ----------------------------------------------------------------------------

"""Module for the zlib (de)compression of objects.inv data block."""


import os
import zlib


BUFSIZE = 16*1024    # 16k chunks


def decompress(bstr):
    """Decompress a version 2 |isphx| ``objects.inv`` bytestring.

    The `#`-prefixed comment lines are left unchanged, whereas the
    :mod:`zlib`-compressed data lines are decompressed to plaintext.

    Parameters
    ----------
    bstr

        |bytes| -- Binary string containing a compressed ``objects.inv``
        file.

    Returns
    -------
    out_b

        |bytes| -- Decompressed binary string containing the plaintext
        ``objects.inv`` content.

    """
    import io

    from .error import VersionError

    def decompress_chunks(bstrm):
        """Handle chunk-wise zlib decompression.

        Internal function pulled from intersphinx.py@v1.4.1:
        https://github.com/sphinx-doc/sphinx/blob/1.4.1/sphinx/
          ext/intersphinx.py#L79-L124.
        BUFSIZE taken as the default value from intersphinx signature
        Modified slightly to take the stream as a parameter,
        rather than assuming one from the parent namespace.

        """
        decompressor = zlib.decompressobj()
        for chunk in iter(lambda: bstrm.read(BUFSIZE), b''):
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    # Make stream and output string
    strm = io.BytesIO(bstr)

    # Check to be sure it's v2
    out_b = strm.readline()
    if not out_b.endswith(b'2\n'):
        raise VersionError('Only v2 objects.inv files currently supported')

    # Pull name, version, and description lines
    for i in range(3):
        out_b += strm.readline()

    # Decompress chunks and append
    for chunk in decompress_chunks(strm):
        out_b += chunk

    # Replace newlines with the OS-local newlines
    out_b = out_b.replace(b'\n', os.linesep.encode('utf-8'))

    # Return the newline-composited result
    return out_b


def compress(bstr):
    """Compress a version 2 |isphx| ``objects.inv`` bytestring.

    The `#`-prefixed comment lines are left unchanged, whereas the
    plaintext data lines are compressed with :mod:`zlib`.

    Parameters
    ----------
    bstr

        |bytes| -- Binary string containing the decompressed contents of an
        ``objects.inv`` file.

    Returns
    -------
    out_b

        |bytes| -- Binary string containing the compressed ``objects.inv``
        content.

    """
    from .re import pb_comments, pb_data

    # Preconvert any DOS newlines to Unix
    s = bstr.replace(b'\r\n', b'\n')

    # Pull all of the lines
    m_comments = pb_comments.findall(s)
    m_data = pb_data.finditer(s)

    # Assemble the binary header comments and data
    # Comments and data blocks must end in newlines
    hb = b'\n'.join(m_comments) + b'\n'
    db = b'\n'.join(_.group(0) for _ in m_data) + b'\n'

    # Compress the data block
    # Compression level nine is to match that specified in
    #  sphinx html builder:
    # https://github.com/sphinx-doc/sphinx/blob/1.4.1/sphinx/
    #    builders/html.py#L843
    dbc = zlib.compress(db, 9)

    # Return the composited bytestring
    return hb + dbc


if __name__ == '__main__':    # pragma: no cover
    print('Module not executable.')
