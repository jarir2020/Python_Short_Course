"""Transform Task model instances to and from validated API data."""

from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Expose safe task fields while keeping ownership server-controlled."""

    class Meta:
        model = Task
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def validate_title(self, value: str) -> str:
        """Reject whitespace-only titles before Django writes the model."""

        cleaned_title = value.strip()
        if not cleaned_title:
            raise serializers.ValidationError("Title must contain visible text.")
        return cleaned_title
