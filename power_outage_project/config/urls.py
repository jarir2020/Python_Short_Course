"""Top-level URL configuration for PowerTrack."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.routes")),
    path("api/", include("outages.routes")),
]
