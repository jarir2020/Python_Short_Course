"""ASGI entry point for the PowerTrack FastAPI read service."""

from fastapi import FastAPI

from .routes import router


app = FastAPI(
    title="PowerTrack Operations API",
    description=(
        "Read-only operations views backed by the PowerTrack Django API. "
        "This service never writes to Django's database."
    ),
    version="1.0.0",
)
app.include_router(router, prefix="/api")


@app.get("/api/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "framework": "fastapi", "service": "powertrack-operations"}
