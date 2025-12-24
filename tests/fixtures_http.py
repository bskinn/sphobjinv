r"""*HTTP server fixtures definitions for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (brian.skinn@gmail.com)

**File Created**
    24 Dec 2025

**Copyright**
    \(c) Brian Skinn 2016-2025

**Source Repository**
    http://www.github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/stable

**License**
    Code: `MIT License`_

    Docs & Docstrings: |CC BY 4.0|_

    See |license_txt|_ for full license terms.

**Members**

"""

import contextlib
import functools
import http.server
import threading
from pathlib import Path
from typing import Callable, Generator

import pytest


class NoReverseDNSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that skips reverse DNS lookup when logging."""

    def address_string(self) -> str:
        """Return the address string without reverse DNS lookup."""
        return self.client_address[0]


@contextlib.contextmanager
def _baseurl_for_served_directory(
    directory: Path | str, host: str = "localhost"
) -> Generator[str, None, None]:
    """Spin up HTTP server on a directory and yield the server base URL."""
    directory = Path(directory).resolve()

    handler_cls = functools.partial(
        NoReverseDNSRequestHandler,
        directory=str(directory),
    )

    # Bind to port 0 so the OS chooses a free ephemeral port
    httpd = http.server.HTTPServer((host, 0), handler_cls)
    port = httpd.server_address[1]
    base_url = f"http://{host}:{port}"

    thread = threading.Thread(
        target=httpd.serve_forever,
        name="pytest-http-server",
        daemon=True,
    )

    thread.start()

    try:
        yield base_url
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


@pytest.fixture(scope="session")
def resource_http_base_url() -> Generator[str, None, None]:
    """Provide base URL of HTTP server exposing tests/resource/*."""  # noqa: RST213
    resource_dir = Path(__file__).resolve().parent / "resource"

    if not resource_dir.is_dir():
        raise RuntimeError(
            f"Expected test resource directory not found: {resource_dir}"
        )

    with _baseurl_for_served_directory(resource_dir) as base_url:
        yield base_url


@pytest.fixture(scope="session")
def resource_url(resource_http_base_url: str) -> Callable[[str], str]:
    """Provide a function to calculate the full test-resource URL from a relative URL.

    Forbids '..' path segments to avoid root escape.

    **Examples**

    resource_url("objects_bokeh.inv") -> "http://127.0.0.1:{PORT}/objects_bokeh.inv"
    resource_url("subdir/file.ext")   -> ".../subdir/file.ext"

    """

    def _calc_path(rel_path: str) -> str:
        """Calculate the full test-resource URL from a relative URL."""
        # Prevent escaping the resource directory.
        if ".." in Path(rel_path).parts:
            raise ValueError("Path must not contain '..'")

        # Ensure consistent URL path separators.
        url_path = "/".join(Path(rel_path).parts)
        return f"{resource_http_base_url}/{url_path}"

    return _calc_path
