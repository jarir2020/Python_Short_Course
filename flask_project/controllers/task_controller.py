"""Flask controllers for task use-cases.

Controllers read request input and return domain results. URL decorators and
JSON response formatting belong in the separate routes package.
"""

from flask import request

from ..db import get_db
from ..models import Task
from ..services import TaskService


def _task_service() -> TaskService:
    return TaskService(get_db())


def list_tasks() -> list[Task]:
    return _task_service().list_all()


def create_task() -> Task:
    return _task_service().create(request.get_json(silent=True))


def get_task(task_id: int) -> Task | None:
    return _task_service().get(task_id)


def update_task(task_id: int) -> Task | None:
    return _task_service().update(task_id, request.get_json(silent=True))


def delete_task(task_id: int) -> bool:
    return _task_service().delete(task_id)
