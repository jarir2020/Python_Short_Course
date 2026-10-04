"""Business rules for the PowerTrack outage workflow."""

from django.db import transaction
from django.utils import timezone

from accounts.models import User
from common.exceptions import WorkflowError
from outages.models import Assignment, OutageReport, ProgressUpdate
from outages.repositories import (
    add_progress_update,
    assign_report,
    create_report,
    visible_reports_for_user,
)


def create_customer_report(customer: User, validated_data: dict) -> OutageReport:
    return create_report(customer, **validated_data)


def list_visible_reports(user: User):
    return visible_reports_for_user(user)


def get_visible_report(user: User, report_id: int):
    return visible_reports_for_user(user).filter(pk=report_id).first()


@transaction.atomic
def assign_technician(
    report: OutageReport,
    technician: User,
    admin_user: User,
    notes: str = "",
) -> Assignment:
    if report.status in {OutageReport.Status.RESOLVED, OutageReport.Status.REJECTED}:
        raise WorkflowError("A resolved or rejected report cannot be assigned.")
    if technician.role != User.Role.TECHNICIAN:
        raise WorkflowError("Only a technician can receive an assignment.")
    return assign_report(report, technician, admin_user, notes)


@transaction.atomic
def update_report_by_admin(report: OutageReport, validated_data: dict) -> OutageReport:
    if report.status == OutageReport.Status.RESOLVED:
        raise WorkflowError("A resolved report is read-only in this first version.")

    for field, value in validated_data.items():
        setattr(report, field, value)
    if report.status == OutageReport.Status.RESOLVED:
        report.resolved_at = timezone.now()
    report.save()
    return report


@transaction.atomic
def add_technician_progress(
    report: OutageReport,
    technician: User,
    status: str,
    message: str,
) -> ProgressUpdate:
    if report.status == OutageReport.Status.RESOLVED:
        raise WorkflowError("A resolved report cannot receive more progress updates.")

    try:
        assignment = report.assignment
    except Assignment.DoesNotExist as error:
        raise WorkflowError("This report has not been assigned yet.") from error

    if assignment.technician_id != technician.id:
        raise WorkflowError("A technician may update only their own assignments.")

    return add_progress_update(assignment, technician, status, message)
