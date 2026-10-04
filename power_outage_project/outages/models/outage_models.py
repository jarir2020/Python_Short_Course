"""Database models for the outage reporting workflow."""

from django.conf import settings
from django.db import models


class OutageReport(models.Model):
    class Status(models.TextChoices):
        REPORTED = "reported", "Reported"
        VERIFIED = "verified", "Verified"
        ASSIGNED = "assigned", "Assigned"
        IN_PROGRESS = "in_progress", "In progress"
        RESOLVED = "resolved", "Resolved"
        REJECTED = "rejected", "Rejected"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="outage_reports",
    )
    area = models.CharField(max_length=120)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REPORTED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "area"]),
        ]

    def __str__(self) -> str:
        return f"Outage #{self.pk} in {self.area}"

    @property
    def progress_updates(self):
        """Expose assignment history conveniently to serializers and views.

        Progress belongs to an assignment in the database, and a report may
        not have an assignment yet. Returning an empty queryset for that
        early state keeps the API response shape stable.
        """

        try:
            return self.assignment.progress_updates.all()
        except Assignment.DoesNotExist:
            return ProgressUpdate.objects.none()


class Assignment(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = "assigned", "Assigned"
        ACCEPTED = "accepted", "Accepted"
        IN_PROGRESS = "in_progress", "In progress"
        RESOLVED = "resolved", "Resolved"
        REJECTED = "rejected", "Rejected"

    outage_report = models.OneToOneField(
        OutageReport,
        on_delete=models.CASCADE,
        related_name="assignment",
    )
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="technician_assignments",
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assignments_created",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ASSIGNED,
    )
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Assignment for outage #{self.outage_report_id}"


class ProgressUpdate(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="progress_updates",
    )
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="progress_updates_created",
    )
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Assignment.Status.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Progress for assignment #{self.assignment_id}"
