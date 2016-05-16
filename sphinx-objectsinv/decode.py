
def main():
    import os, zlib

    # Switch dir
    os.chdir('C:\\')

    # Open the file and read
    with open('objects.inv', 'rb') as f:
        b = f.read()

    # Split by newline followed by a pound sign
    l = b.split(b'\n#')

    # Most of the header is all but the last element
    h = b'\n#'.join(l[:-1])

    # The rest of the header has to be recovered from
    #  the first part of the last element
    i = b'#' + l[-1].split(b'\n')[0] + b'\n'

    # The data has to be reassembled around any incidental
    #  newlines that were present in the compressed stream
    #  before decompression by zlib
    d = zlib.decompress(
                b'\n'.join(l[-1].split(b'\n')[1:])
                        )

    # Write the decoded file
    with open('objects.txt', 'wb') as f:
        f.write(h + b'\n' + i + d)


if __name__ ==  '__main__':
    main()
