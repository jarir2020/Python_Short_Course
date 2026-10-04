"""Backward-compatible exports for the MVC modules.

New code should import controllers and services directly. These exports keep
older learner imports working while the project is reorganized.
"""

from .routes import task_api
from .controllers import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)
from .models import Task
from .services import (
    ALLOWED_FIELDS,
    ALLOWED_STATUSES,
    TaskValidationError,
    validate_task_payload,
)


def serialize_task(value) -> dict[str, object]:
    """Keep the old row serializer name available during the transition."""

    if isinstance(value, Task):
        return value.to_dict()
    return {key: value[key] for key in value.keys()}


__all__ = [
    "ALLOWED_FIELDS",
    "ALLOWED_STATUSES",
    "TaskValidationError",
    "create_task",
    "delete_task",
    "get_task",
    "list_tasks",
    "serialize_task",
    "task_api",
    "update_task",
    "validate_task_payload",
]
