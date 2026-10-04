from collections.abc import AsyncIterator
from pathlib import Path

import aiosqlite
import httpx
import pytest

from capstone_api.config import Settings, get_settings
from capstone_api.database import get_db, initialize_database
from capstone_api.main import app


@pytest.fixture
async def capstone_client(tmp_path: Path) -> AsyncIterator[httpx.AsyncClient]:
    database_path = tmp_path / "capstone.sqlite3"
    settings = Settings(
        secret_key="test-secret-that-is-at-least-32-bytes-long",
        database_path=database_path,
        rate_limit_requests=100,
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


async def register_and_login(
    client: httpx.AsyncClient,
    username: str,
) -> str:
    registration = await client.post(
        "/api/auth/register",
        json={"username": username, "password": "correct-horse"},
    )
    assert registration.status_code == 201
    token_response = await client.post(
        "/api/auth/token",
        data={"username": username, "password": "correct-horse"},
    )
    assert token_response.status_code == 200
    return token_response.json()["access_token"]


@pytest.mark.anyio
async def test_public_health_has_security_headers(capstone_client: httpx.AsyncClient) -> None:
    response = await capstone_client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "capstone-api"}
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


@pytest.mark.anyio
async def test_registration_login_and_owner_scoped_tasks(
    capstone_client: httpx.AsyncClient,
) -> None:
    alice_token = await register_and_login(capstone_client, "alice")
    bob_token = await register_and_login(capstone_client, "bob")

    task_response = await capstone_client.post(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {alice_token}"},
        json={"title": "Private task"},
    )
    assert task_response.status_code == 201
    task = task_response.json()
    assert task["owner_id"] == 1
    assert "password_hash" not in task

    alice_tasks = await capstone_client.get(
        "/api/tasks/",
        headers={"Authorization": f"Bearer {alice_token}"},
    )
    bob_view = await capstone_client.get(
        f"/api/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {bob_token}"},
    )

    assert len(alice_tasks.json()) == 1
    assert bob_view.status_code == 404


@pytest.mark.anyio
async def test_missing_or_tampered_credentials_are_rejected(
    capstone_client: httpx.AsyncClient,
) -> None:
    missing = await capstone_client.get("/api/tasks/")
    tampered = await capstone_client.get(
        "/api/tasks/",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert missing.status_code == 401
    assert tampered.status_code == 401
    assert tampered.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.anyio
async def test_invalid_password_and_duplicate_user_are_safe_errors(
    capstone_client: httpx.AsyncClient,
) -> None:
    first = await capstone_client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "correct-horse"},
    )
    duplicate = await capstone_client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "correct-horse"},
    )
    invalid_login = await capstone_client.post(
        "/api/auth/token",
        data={"username": "alice", "password": "wrong-password"},
    )

    assert first.status_code == 201
    assert duplicate.status_code == 409
    assert invalid_login.status_code == 401


@pytest.mark.anyio
async def test_pydantic_rejects_short_password_and_openapi_describes_bearer_auth(
    capstone_client: httpx.AsyncClient,
) -> None:
    invalid = await capstone_client.post(
        "/api/auth/register",
        json={"username": "short", "password": "tiny"},
    )
    schema = (await capstone_client.get("/openapi.json")).json()

    assert invalid.status_code == 422
    assert "OAuth2PasswordBearer" in schema["components"]["securitySchemes"]
