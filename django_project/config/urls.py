"""Top-level URL configuration for the task API."""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(request):
    """A public endpoint used to confirm that Django is running."""

    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/", include("django_project.tasks.routes")),
    path("api-auth/", include("rest_framework.urls")),
]
