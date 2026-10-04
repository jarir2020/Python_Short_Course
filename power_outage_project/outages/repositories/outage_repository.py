"""ORM operations for outage reports and their workflow records."""

from django.db import transaction
from django.utils import timezone

from accounts.models import User
from outages.models import Assignment, OutageReport, ProgressUpdate


def _report_queryset():
    """Load related people and progress in predictable database queries."""

    return OutageReport.objects.select_related(
        "customer",
        "assignment__technician",
        "assignment__assigned_by",
    ).prefetch_related("assignment__progress_updates")


def visible_reports_for_user(user: User):
    """Return only reports the caller is allowed to discover."""

    queryset = _report_queryset()
    if user.role == User.Role.ADMIN:
        return queryset
    if user.role == User.Role.TECHNICIAN:
        return queryset.filter(assignment__technician=user)
    return queryset.filter(customer=user)


def get_report(report_id: int):
    return _report_queryset().filter(pk=report_id).first()


def create_report(customer: User, **validated_data) -> OutageReport:
    return OutageReport.objects.create(customer=customer, **validated_data)


@transaction.atomic
def assign_report(
    report: OutageReport,
    technician: User,
    admin_user: User,
    notes: str = "",
) -> Assignment:
    """Create or replace the one active assignment for a report."""

    assignment, _ = Assignment.objects.update_or_create(
        outage_report=report,
        defaults={
            "technician": technician,
            "assigned_by": admin_user,
            "status": Assignment.Status.ASSIGNED,
            "notes": notes,
        },
    )
    report.status = OutageReport.Status.ASSIGNED
    report.resolved_at = None
    report.save(update_fields=["status", "resolved_at", "updated_at"])
    return assignment


@transaction.atomic
def add_progress_update(
    assignment: Assignment,
    technician: User,
    status: str,
    message: str,
) -> ProgressUpdate:
    """Persist a progress event and synchronize the parent records."""

    progress = ProgressUpdate.objects.create(
        assignment=assignment,
        technician=technician,
        status=status,
        message=message,
    )
    assignment.status = status
    assignment.save(update_fields=["status", "updated_at"])

    report = assignment.outage_report
    report_status_by_assignment = {
        Assignment.Status.ASSIGNED: OutageReport.Status.ASSIGNED,
        Assignment.Status.ACCEPTED: OutageReport.Status.ASSIGNED,
        Assignment.Status.IN_PROGRESS: OutageReport.Status.IN_PROGRESS,
        Assignment.Status.RESOLVED: OutageReport.Status.RESOLVED,
        Assignment.Status.REJECTED: OutageReport.Status.VERIFIED,
    }
    report.status = report_status_by_assignment[status]
    report.resolved_at = timezone.now() if status == Assignment.Status.RESOLVED else None
    report.save(update_fields=["status", "resolved_at", "updated_at"])
    return progress
