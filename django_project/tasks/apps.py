from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Application configuration Django uses while loading the tasks app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_project.tasks"
