"""Reusable role permissions for DRF controllers."""

from rest_framework.permissions import BasePermission

from accounts.models import User


class RolePermission(BasePermission):
    """Base class that turns a user role into a request permission."""

    required_role: str | None = None

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == self.required_role
        )


class IsAdminRole(RolePermission):
    required_role = User.Role.ADMIN


class IsTechnicianRole(RolePermission):
    required_role = User.Role.TECHNICIAN


class IsCustomerRole(RolePermission):
    required_role = User.Role.CUSTOMER
