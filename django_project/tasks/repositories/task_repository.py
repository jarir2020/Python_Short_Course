"""Database operations for tasks, isolated behind small functions."""

from django.db.models import QuerySet

from ..models import Task


def list_tasks_for_user(user) -> QuerySet[Task]:
    """Return only tasks owned by the authenticated user."""

    return Task.objects.filter(owner=user)


def create_task(serializer, user) -> Task:
    """Persist validated serializer data with server-controlled ownership."""

    return serializer.save(owner=user)
