"""The custom user used by every PowerTrack workflow."""

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class PowerTrackUserManager(UserManager):
    """Ensure Django-created superusers also receive the admin role."""

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", PowerTrackUser.Role.ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """A normal Django user plus the business role used by the API.

    Django's ``is_staff`` and ``is_superuser`` flags control access to the
    built-in admin site. ``role`` controls PowerTrack business permissions;
    keeping both ideas separate makes the workflow easier to understand.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        TECHNICIAN = "technician", "Technician"
        CUSTOMER = "customer", "Customer"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone = models.CharField(max_length=30, blank=True)
    area = models.CharField(max_length=120, blank=True)

    objects = PowerTrackUserManager()

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"
