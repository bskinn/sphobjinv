# Quickie script for refreshing the local objects.inv cache
# OVERWRITES EXISTING FILES, WITH PRE-DELETION



def pullobjs():

    import os
    import urllib.request as urlrq
    import wget

    import certifi

    # Open conf.py, retrieve content and compile
    with open(os.path.join(os.pardir, 'conf.py'), 'r') as f:
        confcode = compile(f.read(), 'conf.py', 'exec')

    # Execute conf.py into the global namespace (I know, sloppy)
    exec(confcode, globals())

    # Iterate intersphinx_mapping from conf.py to retrieve the objects.inv files
    # Make use of the conf.py 'isphx_objstr' substitution string, too
    for n, t in intersphinx_mapping.items():

        print('{0}:'.format(n))

        try:
            os.remove(isphx_objstr.format(n))
        except FileNotFoundError:
            pass # No big deal

        #wget.download(url=t[0] + '/objects.inv', out=isphx_objstr.format(n))
        resp = urlrq.urlopen(t[0] + '/objects.inv', cafile=certifi.where())
        with open(isphx_objstr.format(n), 'wb') as f:
            f.write(resp.read())

        print('... Done.\n\n')


if __name__ == '__main__':

    pullobjs()


