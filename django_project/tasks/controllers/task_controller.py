"""Django ViewSet controllers for task HTTP actions.

Django calls this layer a View in MVT. It coordinates serializers and services
while the ORM model and repository own persistence details.
"""

from rest_framework import permissions, viewsets

from ..models import Task
from ..serializers import TaskSerializer
from ..services import create_task_for_user, list_user_tasks


class TaskViewSet(viewsets.ModelViewSet):
    """Provide CRUD actions for one authenticated user tasks."""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ask the service layer for the current user task queryset."""

        if not self.request.user.is_authenticated:
            return Task.objects.none()
        return list_user_tasks(self.request.user)

    def perform_create(self, serializer: TaskSerializer) -> None:
        """Set ownership from the authenticated request, never request data."""

        create_task_for_user(serializer, self.request.user)
