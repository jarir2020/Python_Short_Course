"""Async data-access functions for the task API."""

from datetime import datetime, timezone

import aiosqlite

from ..models import TaskCreate, TaskRead, TaskStatus, TaskUpdate


def _task_from_row(row: aiosqlite.Row) -> TaskRead:
    """Convert one SQLite row into the public Pydantic response model."""

    return TaskRead.model_validate(dict(row))


async def list_tasks(database: aiosqlite.Connection) -> list[TaskRead]:
    cursor = await database.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    )
    rows = await cursor.fetchall()
    await cursor.close()
    return [_task_from_row(row) for row in rows]


async def get_task(
    database: aiosqlite.Connection,
    task_id: int,
) -> TaskRead | None:
    cursor = await database.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    )
    row = await cursor.fetchone()
    await cursor.close()
    return _task_from_row(row) if row is not None else None


async def create_task(
    database: aiosqlite.Connection,
    payload: TaskCreate,
) -> TaskRead:
    now = datetime.now(timezone.utc).isoformat()
    cursor = await database.execute(
        """
        INSERT INTO tasks (title, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload.title,
            payload.description,
            payload.status.value,
            now,
            now,
        ),
    )
    await database.commit()
    created = await get_task(database, cursor.lastrowid)
    await cursor.close()
    assert created is not None
    return created


async def update_task(
    database: aiosqlite.Connection,
    task_id: int,
    payload: TaskUpdate,
) -> TaskRead | None:
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)
    if not changes:
        return await get_task(database, task_id)

    assignments: list[str] = []
    values: list[str] = []
    for field, value in changes.items():
        assignments.append(f"{field} = ?")
        values.append(value.value if isinstance(value, TaskStatus) else value)

    assignments.append("updated_at = ?")
    values.append(datetime.now(timezone.utc).isoformat())
    values.append(task_id)

    cursor = await database.execute(
        f"UPDATE tasks SET {', '.join(assignments)} WHERE id = ?",
        tuple(values),
    )
    await database.commit()
    await cursor.close()
    return await get_task(database, task_id)


async def delete_task(database: aiosqlite.Connection, task_id: int) -> bool:
    cursor = await database.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    await database.commit()
    deleted = cursor.rowcount == 1
    await cursor.close()
    return deleted
