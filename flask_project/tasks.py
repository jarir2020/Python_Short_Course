"""Blueprint routes for the Flask task API."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from .db import get_db


class TaskValidationError(ValueError):
    """Raised when a JSON task payload violates the API contract."""


task_api = Blueprint("task_api", __name__)
ALLOWED_STATUSES = {"todo", "in_progress", "done"}
ALLOWED_FIELDS = {"title", "description", "status"}


def validate_task_payload(payload: object, *, partial: bool = False) -> dict[str, str]:
    """Validate and normalize a JSON object before SQL receives it."""

    if not isinstance(payload, dict):
        raise TaskValidationError("JSON body must be an object.")

    unknown_fields = set(payload) - ALLOWED_FIELDS
    if unknown_fields:
        raise TaskValidationError(
            f"Unknown field(s): {', '.join(sorted(unknown_fields))}."
        )

    if not partial and "title" not in payload:
        raise TaskValidationError("title is required.")
    if partial and not payload:
        raise TaskValidationError("At least one field is required.")

    cleaned: dict[str, str] = {}
    if "title" in payload:
        title = payload["title"]
        if not isinstance(title, str) or not title.strip():
            raise TaskValidationError("title must contain visible text.")
        cleaned["title"] = title.strip()

    if "description" in payload:
        description = payload["description"]
        if not isinstance(description, str):
            raise TaskValidationError("description must be a string.")
        cleaned["description"] = description

    if "status" in payload:
        status = payload["status"]
        if status not in ALLOWED_STATUSES:
            raise TaskValidationError(
                f"status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}."
            )
        cleaned["status"] = status

    return cleaned


def serialize_task(row) -> dict[str, object]:
    """Convert a SQLite row into JSON-friendly API data."""

    return {key: row[key] for key in row.keys()}


@task_api.get("/health")
def health():
    """Return a public health response."""

    return jsonify(status="ok", framework="flask")


@task_api.get("/tasks")
def list_tasks():
    database = get_db()
    rows = database.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return jsonify([serialize_task(row) for row in rows])


@task_api.post("/tasks")
def create_task():
    payload = validate_task_payload(request.get_json(silent=True))
    now = datetime.now(timezone.utc).isoformat()
    database = get_db()
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
    row = database.execute(
        "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify(serialize_task(row)), 201


@task_api.get("/tasks/<int:task_id>")
def get_task(task_id: int):
    row = get_db().execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    if row is None:
        return jsonify(error="not_found", message="Task not found"), 404
    return jsonify(serialize_task(row))


@task_api.patch("/tasks/<int:task_id>")
def update_task(task_id: int):
    payload = validate_task_payload(request.get_json(silent=True), partial=True)
    database = get_db()
    assignments = [f"{field} = ?" for field in payload]
    values = list(payload.values())
    assignments.append("updated_at = ?")
    values.append(datetime.now(timezone.utc).isoformat())
    values.append(task_id)
    cursor = database.execute(
        f"UPDATE tasks SET {', '.join(assignments)} WHERE id = ?",
        values,
    )
    database.commit()
    if cursor.rowcount != 1:
        return jsonify(error="not_found", message="Task not found"), 404
    row = database.execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    return jsonify(serialize_task(row))


@task_api.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    database = get_db()
    cursor = database.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    database.commit()
    if cursor.rowcount != 1:
        return jsonify(error="not_found", message="Task not found"), 404
    return "", 204
