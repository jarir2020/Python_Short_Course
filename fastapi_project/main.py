"""FastAPI application entry point for Phase 4."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from .database import initialize_database
from .routes import router as task_router
from .models import HealthResponse


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize resources before serving and release them on shutdown."""

    await initialize_database()
    yield


app = FastAPI(
    title="Phase 4 Task API",
    description="A small FastAPI and Pydantic learning service.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(task_router, prefix="/api")


@app.get("/api/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    """Return a typed health response."""

    return HealthResponse(status="ok", framework="fastapi")
