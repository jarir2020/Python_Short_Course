"""Async SQLite connection and schema dependencies."""

from collections.abc import AsyncIterator
from pathlib import Path

import aiosqlite


DATABASE_PATH = Path(__file__).resolve().parent / "fastapi.sqlite3"

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'todo',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
"""


async def initialize_database(path: Path = DATABASE_PATH) -> None:
    """Create the table required by the API if it does not exist."""

    async with aiosqlite.connect(path) as database:
        await database.execute(CREATE_TASKS_TABLE)
        await database.commit()


async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    """Yield one async database connection per request.

    FastAPI sees this function through ``Depends(get_db)``. The ``yield``
    pattern gives the route a live connection and guarantees it is closed
    after the response, even if the route raises an exception.
    """

    database = await aiosqlite.connect(DATABASE_PATH)
    database.row_factory = aiosqlite.Row
    try:
        yield database
    finally:
        await database.close()
