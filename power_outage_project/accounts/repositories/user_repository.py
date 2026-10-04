"""Database operations for accounts.

The repository is deliberately small. Its purpose is to keep ORM calls out
of controllers and to make the data boundary visible to a learner.
"""

from accounts.models import User


def create_customer(**validated_data) -> User:
    """Create a customer while preventing public registration as staff."""

    return User.objects.create_user(
        role=User.Role.CUSTOMER,
        **validated_data,
    )
