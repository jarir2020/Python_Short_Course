"""Liveness and readiness route registration."""

import aiosqlite
from fastapi import APIRouter, HTTPException, status

from ..dependencies import Database


health_router = APIRouter(prefix="/health", tags=["health"])


async def liveness() -> dict[str, str]:
    return {"status": "ok", "check": "liveness"}


async def readiness(database: Database) -> dict[str, str]:
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


health_router.add_api_route("/live", liveness, methods=["GET"])
health_router.add_api_route("/ready", readiness, methods=["GET"])
