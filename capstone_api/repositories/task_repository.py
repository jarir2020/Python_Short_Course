"""Async persistence functions kept separate from HTTP route handlers."""

from dataclasses import dataclass
from datetime import datetime, timezone

import aiosqlite

from ..models import TaskCreate, TaskRead, TaskStatus, TaskUpdate


@dataclass(frozen=True)
class StoredUser:
    """Internal user record that includes the hash but is never serialized directly."""

    id: int
    username: str
    password_hash: str
    created_at: str


def _user_from_row(row: aiosqlite.Row) -> StoredUser:
    return StoredUser(
        id=row["id"],
        username=row["username"],
        password_hash=row["password_hash"],
        created_at=row["created_at"],
    )


async def find_user(
    database: aiosqlite.Connection,
    username: str,
) -> StoredUser | None:
    cursor = await database.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    )
    row = await cursor.fetchone()
    await cursor.close()
    return _user_from_row(row) if row else None


async def create_user(
    database: aiosqlite.Connection,
    username: str,
    password_hash: str,
) -> StoredUser:
    now = datetime.now(timezone.utc).isoformat()
    cursor = await database.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, password_hash, now),
    )
    await database.commit()
    user = await find_user(database, username)
    await cursor.close()
    assert user is not None
    return user


def _task_from_row(row: aiosqlite.Row) -> TaskRead:
    return TaskRead.model_validate(dict(row))


async def list_tasks(
    database: aiosqlite.Connection,
    owner_id: int,
) -> list[TaskRead]:
    cursor = await database.execute(
        "SELECT * FROM tasks WHERE owner_id = ? ORDER BY id DESC",
        (owner_id,),
    )
    rows = await cursor.fetchall()
    await cursor.close()
    return [_task_from_row(row) for row in rows]


async def get_task(
    database: aiosqlite.Connection,
    task_id: int,
    owner_id: int,
) -> TaskRead | None:
    cursor = await database.execute(
        "SELECT * FROM tasks WHERE id = ? AND owner_id = ?",
        (task_id, owner_id),
    )
    row = await cursor.fetchone()
    await cursor.close()
    return _task_from_row(row) if row else None


async def create_task(
    database: aiosqlite.Connection,
    owner_id: int,
    payload: TaskCreate,
) -> TaskRead:
    now = datetime.now(timezone.utc).isoformat()
    cursor = await database.execute(
        """
        INSERT INTO tasks
            (owner_id, title, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            owner_id,
            payload.title,
            payload.description,
            payload.status.value,
            now,
            now,
        ),
    )
    await database.commit()
    task = await get_task(database, cursor.lastrowid, owner_id)
    await cursor.close()
    assert task is not None
    return task


async def update_task(
    database: aiosqlite.Connection,
    task_id: int,
    owner_id: int,
    payload: TaskUpdate,
) -> TaskRead | None:
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)
    if not changes:
        return await get_task(database, task_id, owner_id)

    assignments: list[str] = []
    values: list[object] = []
    for field, value in changes.items():
        assignments.append(f"{field} = ?")
        values.append(value.value if isinstance(value, TaskStatus) else value)

    assignments.append("updated_at = ?")
    values.append(datetime.now(timezone.utc).isoformat())
    values.extend([task_id, owner_id])
    cursor = await database.execute(
        f"UPDATE tasks SET {', '.join(assignments)} "
        "WHERE id = ? AND owner_id = ?",
        tuple(values),
    )
    await database.commit()
    await cursor.close()
    return await get_task(database, task_id, owner_id)


async def delete_task(
    database: aiosqlite.Connection,
    task_id: int,
    owner_id: int,
) -> bool:
    cursor = await database.execute(
        "DELETE FROM tasks WHERE id = ? AND owner_id = ?",
        (task_id, owner_id),
    )
    await database.commit()
    deleted = cursor.rowcount == 1
    await cursor.close()
    return deleted
