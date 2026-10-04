"""Business operations for user accounts."""

from accounts.models import User
from accounts.repositories import create_customer


def register_customer(validated_data: dict) -> User:
    """Register only a customer through the public API.

    Admins can create technicians from the admin site or a future protected
    admin endpoint. Allowing a public request to submit ``role=admin`` would
    be an authorization bug, so the role is assigned inside this service.
    """

    return create_customer(**validated_data)
