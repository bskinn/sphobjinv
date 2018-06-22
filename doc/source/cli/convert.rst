.. Description of convert commandline usage

Command-Line Usage: "convert" Mode
==================================

.. program:: sphobjinv convert

The |cour|\ convert\ |/cour| subparser is used for all conversions of inventory
files among plaintext, zlib-compressed, and (unique to |soi|) JSON formats.
Currently, the |soi| CLI can read |objects.inv| files from local files
in any of these three formats, as well as standard zlib-compressed files
from remote locations (see :option:`--url`). At the moment, the only output
method supported is writing to a local file.

.. note::

    If reading from |stdin| or writing to |stdout| would be useful to you,
    please leave a note at :issue:`74` so I can gauge interest.
