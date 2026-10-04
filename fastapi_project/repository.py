"""Compatibility exports; new code should import from ``repositories``."""

from .repositories.task_repository import create_task, delete_task, get_task, list_tasks, update_task

__all__ = ["create_task", "delete_task", "get_task", "list_tasks", "update_task"]
