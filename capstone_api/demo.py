"""Run the capstone flow: register, login, and create an owned task."""

import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import AsyncIterator

import aiosqlite
import httpx

from .config import Settings, get_settings
from .database import get_db, initialize_database
from .main import app


async def main() -> None:
    with TemporaryDirectory() as directory:
        settings = Settings(
            secret_key="demo-secret-that-is-at-least-32-bytes-long",
            database_path=Path(directory) / "capstone.sqlite3",
        )
        await initialize_database(settings.database_path)

        async def override_settings() -> Settings:
            return settings

        async def override_db() -> AsyncIterator[aiosqlite.Connection]:
            database = await aiosqlite.connect(settings.database_path)
            database.row_factory = aiosqlite.Row
            try:
                yield database
            finally:
                await database.close()

        app.dependency_overrides[get_settings] = override_settings
        app.dependency_overrides[get_db] = override_db
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://test",
            ) as client:
                registration = await client.post(
                    "/api/auth/register",
                    json={"username": "demo", "password": "correct-horse"},
                )
                token_response = await client.post(
                    "/api/auth/token",
                    data={"username": "demo", "password": "correct-horse"},
                )
                token = token_response.json()["access_token"]
                task_response = await client.post(
                    "/api/tasks/",
                    headers={"Authorization": f"Bearer {token}"},
                    json={"title": "Review security boundaries"},
                )
                print(registration.json())
                print(token_response.status_code)
                print(task_response.json())
        finally:
            app.dependency_overrides.clear()


if __name__ == "__main__":
    asyncio.run(main())
