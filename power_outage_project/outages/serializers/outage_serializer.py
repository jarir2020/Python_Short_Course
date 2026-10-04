"""Serializers that define the public outage API contract."""

from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserReadSerializer
from outages.models import Assignment, OutageReport, ProgressUpdate


class OutageReportCreateSerializer(serializers.ModelSerializer):
    """Customer input; server-controlled fields are intentionally omitted."""

    class Meta:
        model = OutageReport
        fields = ["area", "description"]


class AssignmentReadSerializer(serializers.ModelSerializer):
    technician = UserReadSerializer(read_only=True)
    assigned_by = UserReadSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id",
            "technician",
            "assigned_by",
            "assigned_at",
            "updated_at",
            "status",
            "notes",
        ]


class ProgressUpdateReadSerializer(serializers.ModelSerializer):
    technician = UserReadSerializer(read_only=True)

    class Meta:
        model = ProgressUpdate
        fields = ["id", "technician", "message", "status", "created_at"]


class OutageReportReadSerializer(serializers.ModelSerializer):
    customer = UserReadSerializer(read_only=True)
    assignment = AssignmentReadSerializer(read_only=True, allow_null=True)
    progress_updates = ProgressUpdateReadSerializer(many=True, read_only=True)

    class Meta:
        model = OutageReport
        fields = [
            "id",
            "customer",
            "area",
            "description",
            "priority",
            "status",
            "created_at",
            "updated_at",
            "resolved_at",
            "assignment",
            "progress_updates",
        ]


class AssignTechnicianSerializer(serializers.Serializer):
    technician = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(
            role=User.Role.TECHNICIAN,
            is_active=True,
        )
    )
    notes = serializers.CharField(required=False, allow_blank=True)


class AdminOutageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutageReport
        fields = ["priority", "status"]


class ProgressUpdateCreateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Assignment.Status.choices)
    message = serializers.CharField()
