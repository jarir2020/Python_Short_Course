"""Business rules and use-cases for Flask task controllers."""

from ..models import Task
from ..repositories import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)


class TaskValidationError(ValueError):
    """Raised when a JSON task payload violates the API contract."""


ALLOWED_STATUSES = {"todo", "in_progress", "done"}
ALLOWED_FIELDS = {"title", "description", "status"}


def validate_task_payload(payload: object, *, partial: bool = False) -> dict[str, str]:
    """Validate and normalize an input object before it reaches the service."""

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
        task_status = payload["status"]
        if task_status not in ALLOWED_STATUSES:
            raise TaskValidationError(
                f"status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}."
            )
        cleaned["status"] = task_status

    return cleaned


class TaskService:
    """Expose task use-cases to controllers without HTTP concerns."""

    def __init__(self, database):
        self.database = database

    def list_all(self) -> list[Task]:
        return list_tasks(self.database)

    def create(self, payload: object) -> Task:
        return create_task(self.database, validate_task_payload(payload))

    def get(self, task_id: int) -> Task | None:
        return get_task(self.database, task_id)

    def update(self, task_id: int, payload: object) -> Task | None:
        cleaned = validate_task_payload(payload, partial=True)
        return update_task(self.database, task_id, cleaned)

    def delete(self, task_id: int) -> bool:
        return delete_task(self.database, task_id)
