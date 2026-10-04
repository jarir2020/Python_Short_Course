"""Business use-cases for the Django task controller."""

from ..repositories import create_task, list_tasks_for_user


def list_user_tasks(user):
    """Coordinate the owner-scoped task listing use-case."""

    return list_tasks_for_user(user)


def create_task_for_user(serializer, user):
    """Coordinate creation while keeping ownership outside request data."""

    return create_task(serializer, user)
