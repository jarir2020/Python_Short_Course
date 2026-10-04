from collections.abc import AsyncIterator
from pathlib import Path

import aiosqlite
import httpx
import pytest

from capstone_api.config import Settings, get_settings
from capstone_api.database import get_db, initialize_database
from capstone_api.main import app


@pytest.fixture
async def phase7_client(tmp_path: Path) -> AsyncIterator[httpx.AsyncClient]:
    """Use a temporary database so this test cannot change local demo data."""

    database_path = tmp_path / "phase7.sqlite3"
    settings = Settings(
        secret_key="phase7-test-secret-that-is-at-least-32-bytes",
        database_path=database_path,
    )
    await initialize_database(database_path)

    async def override_settings() -> Settings:
        return settings

    async def override_db() -> AsyncIterator[aiosqlite.Connection]:
        database = await aiosqlite.connect(database_path)
        database.row_factory = aiosqlite.Row
        try:
            yield database
        finally:
            await database.close()

    app.dependency_overrides[get_settings] = override_settings
    app.dependency_overrides[get_db] = override_db
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_liveness_and_readiness_are_different_checks(
    phase7_client: httpx.AsyncClient,
) -> None:
    live = await phase7_client.get("/api/health/live")
    ready = await phase7_client.get(
        "/api/health/ready",
        headers={"X-Request-ID": "lesson-7"},
    )

    assert live.json() == {"status": "ok", "check": "liveness"}
    assert ready.json() == {
        "status": "ok",
        "check": "readiness",
        "database": "ok",
    }
    assert ready.headers["X-Request-ID"] == "lesson-7"
    assert float(ready.headers["X-Process-Time"]) >= 0


@pytest.mark.anyio
async def test_request_id_is_safe_and_correlated(
    phase7_client: httpx.AsyncClient,
) -> None:
    response = await phase7_client.get(
        "/api/health/live",
        headers={"X-Request-ID": "lesson-7"},
    )

    assert response.headers["X-Request-ID"] == "lesson-7"
    assert float(response.headers["X-Process-Time"]) >= 0
