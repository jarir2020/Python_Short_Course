"""A local HTTP lab for requests, responses, methods, and JSON.

The server in this module runs only on localhost and is useful for learning
because each request is deterministic. It shows the same request/response
shape used when a Python client talks to a real backend over the network.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from threading import Thread
from typing import Any, Iterator, Mapping
from urllib.parse import urlparse

import requests


@dataclass(frozen=True)
class HttpResponse:
    """The useful parts of an HTTP response in a small, testable object."""

    status_code: int
    headers: dict[str, str]
    body: Any


def describe_http_methods() -> dict[str, dict[str, bool]]:
    """Summarize common method properties from HTTP theory.

    A safe method should not change server state. An idempotent method has the
    same intended effect when repeated, even if the response differs.
    ``PATCH`` is not guaranteed to be idempotent because it depends on the
    patch operation itself.
    """

    return {
        "GET": {"safe": True, "idempotent": True},
        "POST": {"safe": False, "idempotent": False},
        "PUT": {"safe": False, "idempotent": True},
        "PATCH": {"safe": False, "idempotent": False},
        "DELETE": {"safe": False, "idempotent": True},
    }


def request_json(
    url: str,
    method: str = "GET",
    payload: Mapping[str, object] | None = None,
    timeout: float = 5.0,
) -> HttpResponse:
    """Send a JSON-capable HTTP request and return its parsed response.

    ``requests`` handles details such as opening the connection, encoding the
    JSON body, and decoding response headers. The request still follows the
    ordinary HTTP model: method + URL + headers + optional body.
    """

    normalized_method = method.upper()
    if normalized_method not in describe_http_methods():
        raise ValueError(f"Unsupported teaching method: {method}")

    request_options: dict[str, object] = {"timeout": timeout}
    if payload is not None:
        # Passing ``json=`` tells requests to serialize the mapping and set an
        # appropriate Content-Type header instead of manually building JSON.
        request_options["json"] = dict(payload)

    response = requests.request(normalized_method, url, **request_options)
    body: Any = response.json() if response.content else None

    return HttpResponse(
        status_code=response.status_code,
        headers=dict(response.headers),
        body=body,
    )


class DemoRequestHandler(BaseHTTPRequestHandler):
    """Return small JSON responses for each HTTP method in the local lab."""

    def log_message(self, format: str, *args: object) -> None:
        """Keep the lesson output focused instead of printing server logs."""

    def _send_json(self, status_code: int, body: object | None = None) -> None:
        encoded_body = b"" if body is None else json.dumps(body).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded_body)))
        self.end_headers()
        if encoded_body:
            self.wfile.write(encoded_body)

    def _read_json(self) -> object:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        return json.loads(raw_body.decode("utf-8")) if raw_body else None

    def do_GET(self) -> None:
        self._send_json(
            200,
            {"method": "GET", "path": urlparse(self.path).path},
        )

    def do_POST(self) -> None:
        self._send_json(201, {"method": "POST", "payload": self._read_json()})

    def do_PUT(self) -> None:
        self._send_json(200, {"method": "PUT", "payload": self._read_json()})

    def do_DELETE(self) -> None:
        # 204 means success with no response body.
        self._send_json(204)


@contextmanager
def demo_server() -> Iterator[str]:
    """Run the local HTTP server for the duration of a ``with`` block."""

    server = ThreadingHTTPServer(("127.0.0.1", 0), DemoRequestHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    host, port = server.server_address
    try:
        yield f"http://{host}:{port}"
    finally:
        # Shutdown unblocks serve_forever; joining the thread prevents a
        # background server from leaking into later tests or lessons.
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


if __name__ == "__main__":
    with demo_server() as base_url:
        print(request_json(f"{base_url}/health").body)
        print(request_json(f"{base_url}/items", "POST", {"name": "book"}).body)
