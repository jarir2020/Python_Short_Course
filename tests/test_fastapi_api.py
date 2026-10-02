from collections.abc import AsyncIterator

import aiosqlite
import httpx
import pytest
from fastapi import FastAPI

from fastapi_project.database import get_db, initialize_database
from fastapi_project.main import app


@pytest.fixture
async def api_client(tmp_path) -> AsyncIterator[httpx.AsyncClient]:
    """Override the DB dependency with an isolated temporary database."""

    database_path = tmp_path / "test.sqlite3"
    await initialize_database(database_path)

    async def override_get_db() -> AsyncIterator[aiosqlite.Connection]:
        database = await aiosqlite.connect(database_path)
        database.row_factory = aiosqlite.Row
        try:
            yield database
        finally:
            await database.close()

    app.dependency_overrides[get_db] = override_get_db
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_health_has_a_typed_response(api_client: httpx.AsyncClient) -> None:
    response = await api_client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "framework": "fastapi"}


@pytest.mark.anyio
async def test_create_list_patch_and_delete_task(
    api_client: httpx.AsyncClient,
) -> None:
    created = await api_client.post(
        "/api/tasks/",
        json={"title": "  Learn Pydantic  ", "status": "todo"},
    )

    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "Learn Pydantic"
    assert task["status"] == "todo"
    task_id = task["id"]

    listed = await api_client.get("/api/tasks/")
    assert [item["id"] for item in listed.json()] == [task_id]

    patched = await api_client.patch(
        f"/api/tasks/{task_id}",
        json={"status": "done"},
    )
    assert patched.status_code == 200
    assert patched.json()["status"] == "done"

    deleted = await api_client.delete(f"/api/tasks/{task_id}")
    assert deleted.status_code == 204
    missing = await api_client.get(f"/api/tasks/{task_id}")
    assert missing.status_code == 404


@pytest.mark.anyio
async def test_pydantic_validation_rejects_blank_title(
    api_client: httpx.AsyncClient,
) -> None:
    response = await api_client.post("/api/tasks/", json={"title": "   "})

    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.anyio
async def test_openapi_documents_routes_and_schemas(
    api_client: httpx.AsyncClient,
) -> None:
    response = await api_client.get("/openapi.json")
    schema = response.json()

    assert response.status_code == 200
    assert "/api/tasks/" in schema["paths"]
    assert "TaskCreate" in schema["components"]["schemas"]
