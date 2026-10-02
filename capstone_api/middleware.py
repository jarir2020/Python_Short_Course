"""Small security/operations middleware examples for the capstone."""

from collections import defaultdict
from time import monotonic

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add defensive browser headers to every response."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        return response


class LoginRateLimitMiddleware(BaseHTTPMiddleware):
    """Limit repeated login attempts per process and client IP.

    This intentionally small implementation is for learning only. Production
    deployments with multiple workers should use a shared store such as Redis,
    otherwise each worker would maintain a separate counter.
    """

    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next) -> Response:
        is_login = request.method == "POST" and request.url.path.endswith("/auth/token")
        if not is_login:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = monotonic()
        recent = [
            timestamp
            for timestamp in self._attempts[client_ip]
            if now - timestamp < self.window_seconds
        ]
        if len(recent) >= self.max_requests:
            retry_after = max(1, int(self.window_seconds - (now - recent[0])))
            return JSONResponse(
                {"detail": "Too many login attempts"},
                status_code=429,
                headers={"Retry-After": str(retry_after)},
            )

        recent.append(now)
        self._attempts[client_ip] = recent
        return await call_next(request)
