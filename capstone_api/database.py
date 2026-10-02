"""Async SQLite database dependency for the capstone."""

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Annotated

import aiosqlite
from fastapi import Depends

from .config import Settings, get_settings


CREATE_SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'todo',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tasks_owner_id ON tasks (owner_id);
"""


async def initialize_database(path: Path | None = None) -> None:
    """Create the capstone schema without storing plaintext passwords."""

    database_path = path or get_settings().database_path
    database_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(database_path) as database:
        await database.executescript(CREATE_SCHEMA)
        await database.commit()


async def get_db(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AsyncIterator[aiosqlite.Connection]:
    """Yield a request-scoped async connection and always close it afterward."""

    database = await aiosqlite.connect(settings.database_path)
    database.row_factory = aiosqlite.Row
    await database.execute("PRAGMA foreign_keys = ON")
    try:
        yield database
    finally:
        await database.close()
