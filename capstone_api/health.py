"""Liveness and readiness endpoints used by process managers and load balancers."""

import aiosqlite
from fastapi import APIRouter, HTTPException, status

from .dependencies import Database


health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("/live")
async def liveness() -> dict[str, str]:
    """Show that the Python process and ASGI application are responding."""

    return {"status": "ok", "check": "liveness"}


@health_router.get("/ready")
async def readiness(database: Database) -> dict[str, str]:
    """Show that the service can reach the dependency it needs to serve traffic."""

    try:
        cursor = await database.execute("SELECT 1")
        await cursor.fetchone()
        await cursor.close()
    except aiosqlite.Error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not ready",
        ) from None

    return {"status": "ok", "check": "readiness", "database": "ok"}
