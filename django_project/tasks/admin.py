from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Make task records easy to inspect in Django's admin site."""

    list_display = ("title", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description", "owner__username")
