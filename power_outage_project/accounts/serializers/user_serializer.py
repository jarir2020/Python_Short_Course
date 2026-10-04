"""API serializers for account input and output."""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import User


class UserReadSerializer(serializers.ModelSerializer):
    """Safe user representation used in API responses."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "phone", "area"]


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    """Validate public registration data without accepting a role field."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone", "area"]

    def validate_password(self, value: str) -> str:
        # Django's validators teach us that authentication input needs more
        # than a database field type check.
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
