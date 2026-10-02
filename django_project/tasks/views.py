"""REST API views for tasks."""

from rest_framework import permissions, viewsets

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Provide list/create/retrieve/update/delete actions for one user's tasks."""

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Limit every action to the authenticated user's own tasks."""

        if not self.request.user.is_authenticated:
            return Task.objects.none()
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer: TaskSerializer) -> None:
        """Set ownership from the authenticated request, never request data."""

        serializer.save(owner=self.request.user)
