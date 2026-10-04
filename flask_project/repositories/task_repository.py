"""SQLite data-access functions for Flask.

Only this layer builds SQL. Controllers and services work with dictionaries
and ``Task`` models instead of knowing table or column details.
"""

from datetime import datetime, timezone

import sqlite3

from ..models import Task


def list_tasks(database: sqlite3.Connection) -> list[Task]:
    rows = database.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return [Task.from_row(row) for row in rows]


def get_task(database: sqlite3.Connection, task_id: int) -> Task | None:
    row = database.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()
    return Task.from_row(row) if row is not None else None


def create_task(database: sqlite3.Connection, payload: dict[str, str]) -> Task:
    now = datetime.now(timezone.utc).isoformat()
    cursor = database.execute(
        """
        INSERT INTO tasks (title, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload["title"],
            payload.get("description", ""),
            payload.get("status", "todo"),
            now,
            now,
        ),
    )
    database.commit()
    created = get_task(database, cursor.lastrowid)
    assert created is not None
    return created


def update_task(
    database: sqlite3.Connection,
    task_id: int,
    payload: dict[str, str],
) -> Task | None:
    # The service has already restricted keys to known column names. Values
    # still use SQL parameters, which prevents SQL injection in user data.
    assignments = [f"{field} = ?" for field in payload]
    values: list[object] = list(payload.values())
    assignments.append("updated_at = ?")
    values.append(datetime.now(timezone.utc).isoformat())
    values.append(task_id)
    cursor = database.execute(
        f"UPDATE tasks SET {', '.join(assignments)} WHERE id = ?",
        values,
    )
    database.commit()
    if cursor.rowcount != 1:
        return None
    return get_task(database, task_id)


def delete_task(database: sqlite3.Connection, task_id: int) -> bool:
    cursor = database.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    database.commit()
    return cursor.rowcount == 1
