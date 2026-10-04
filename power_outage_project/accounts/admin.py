from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class PowerTrackUserAdmin(UserAdmin):
    """Expose the business role and contact fields in Django admin."""

    fieldsets = UserAdmin.fieldsets + (
        ("PowerTrack details", {"fields": ("role", "phone", "area")}),
    )
    list_display = ("username", "email", "role", "area", "is_active")
    list_filter = ("role", "is_active")
