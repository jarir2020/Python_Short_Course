"""Small request-observability middleware for the Phase 7 lesson."""

import logging
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


logger = logging.getLogger("capstone_api.requests")
REQUEST_ID_HEADER = "X-Request-ID"


def _safe_request_id(request: Request) -> str:
    """Reuse a simple client ID or create one without trusting arbitrary text."""

    incoming = request.headers.get(REQUEST_ID_HEADER, "").strip()
    # Restrict the value before putting it into response headers and logs. A
    # newline in a user-controlled header could otherwise confuse log readers.
    if incoming and len(incoming) <= 100 and all(
        character.isalnum() or character in "-_" for character in incoming
    ):
        return incoming
    return uuid4().hex


class RequestObservabilityMiddleware(BaseHTTPMiddleware):
    """Attach a correlation ID and duration to every response.

    The log record intentionally contains metadata only. It never records
    request bodies, passwords, or Authorization headers.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = _safe_request_id(request)
        request.state.request_id = request_id
        started = perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (perf_counter() - started) * 1000
            logger.exception(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round(duration_ms, 2),
                },
            )
            raise

        duration_ms = (perf_counter() - started) * 1000
        response.headers[REQUEST_ID_HEADER] = request_id
        response.headers["X-Process-Time"] = f"{duration_ms / 1000:.6f}"
        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )
        return response
