"""ASGI entry point for the Phase 7 production-architecture lesson."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import initialize_database
from .health import health_router
from .middleware import LoginRateLimitMiddleware, SecurityHeadersMiddleware
from .observability import RequestObservabilityMiddleware
from .routes import auth_router, task_router


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize the database before serving requests."""

    await initialize_database(settings.database_path)
    yield


app = FastAPI(
    title="Phase 7 Capstone API",
    description="A layered, observable, OAuth2/JWT-secured task API.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)
app.add_middleware(
    LoginRateLimitMiddleware,
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestObservabilityMiddleware)
app.include_router(auth_router, prefix="/api")
app.include_router(task_router, prefix="/api")
app.include_router(health_router, prefix="/api")


@app.get("/api/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "capstone-api"}
