import re
from pathlib import Path


def update_readme(*, name, new_ver, path, encoding="utf-8"):
    """Update links to point to specific versions instead of default/main."""
    content = Path(path).read_text(encoding=encoding)

    # new_ver = version_override if version_override else __version__

    # Helper function
    def content_update(content, pattern, sub):
        return re.sub(pattern, sub, content, flags=re.M | re.I)

    # Docs reference updates to current release version, for PyPI
    # This one gets the badge image
    content = content_update(
        content, r"(?<=/readthedocs/{0}/)\S+?(?=\.svg$)".format(name), "v" + new_ver
    )

    # This one gets the RtD links
    content = content_update(
        content, r"(?<={0}\.readthedocs\.io/en/)\S+?(?=/)".format(name), "v" + new_ver
    )

    return content
