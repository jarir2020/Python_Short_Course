"""URL routing for task resources."""

from rest_framework.routers import DefaultRouter

from .views import TaskViewSet


router = DefaultRouter()
# Routers generate consistent list/detail URLs and connect HTTP verbs to the
# ViewSet actions. Register the prefix without a trailing slash.
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
