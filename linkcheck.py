import argparse as ap
import re
import sys
from pathlib import Path

import requests as rq


p_urls = re.compile('http[s]://[^ (){}<>"\n]+', re.I | re.M)


def get_params():
    prs = ap.ArgumentParser()

    prs.add_argument("files", metavar="file", nargs="+")

    ns = prs.parse_args()

    return vars(ns)


def main():
    params = get_params()

    count = 0

    for fn in params["files"]:
        if (pth := Path(fn)).is_file():
            print(fn)
            print("=" * len(fn))
            for mch in p_urls.finditer(pth.read_text()):
                url = mch.group(0)
                print(f"{url}: ", end="")
                resp = rq.get(url)
                print(f"{resp.status_code} {resp.reason}")
            print()
        else:
            print(f"'{fn}' is not a valid file\n")



if __name__ == "__main__":
    sys.exit(main())
