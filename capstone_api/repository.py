"""Compatibility exports; new code should import from ``repositories``."""

from .repositories.task_repository import (
    StoredUser,
    create_task,
    create_user,
    delete_task,
    find_user,
    get_task,
    list_tasks,
    update_task,
)

__all__ = [
    "StoredUser",
    "create_task",
    "create_user",
    "delete_task",
    "find_user",
    "get_task",
    "list_tasks",
    "update_task",
]
