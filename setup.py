import re
from pathlib import Path

from setuptools import setup

NAME = "sphobjinv"

exec_ns = {}
exec(Path("src", "sphobjinv", "version.py").read_text(encoding="utf-8"), exec_ns)
__version__ = exec_ns["__version__"]

version_override = "2.3.1.2"


def readme():
    content = Path("README.md").read_text(encoding="utf-8")

    new_ver = version_override if version_override else __version__

    # Helper function
    def content_update(content, pattern, sub):
        return re.sub(pattern, sub, content, flags=re.M | re.I)

    # Docs reference updates to current release version, for PyPI
    # This one gets the badge image
    content = content_update(
        content, r"(?<=/readthedocs/{0}/)\S+?(?=\.svg$)".format(NAME), "v" + new_ver
    )

    # This one gets the RtD links
    content = content_update(
        content, r"(?<={0}\.readthedocs\.io/en/)\S+?(?=/)".format(NAME), "v" + new_ver
    )

    return content


setup(
    name=NAME,
    long_description=readme(),
    long_description_content_type="text/markdown",
)
