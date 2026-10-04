"""Use-cases for the read-only PowerTrack operations API."""

from typing import Protocol

from pydantic import ValidationError

from ..models.operation_models import (
    OperationsSummary,
    PublicOutage,
    QueueItem,
    ReportSnapshot,
    TechnicianQueue,
    UserSummary,
)
from ..repositories import DjangoUpstreamError


class ReportReader(Protocol):
    """The small repository interface needed by this service layer."""

    async def list_reports(self) -> list[dict]:
        ...


async def read_reports(client: ReportReader) -> list[ReportSnapshot]:
    """Read and validate Django data before business calculations begin."""

    try:
        raw_reports = await client.list_reports()
        return [ReportSnapshot.model_validate(report) for report in raw_reports]
    except ValidationError as error:
        # A changed Django response is an upstream contract error, not a
        # client validation error. The controller converts it to HTTP 502.
        raise DjangoUpstreamError("Django returned an invalid report contract.") from error


def build_summary(reports: list[ReportSnapshot]) -> OperationsSummary:
    reports_by_status: dict[str, int] = {}
    for report in reports:
        reports_by_status[report.status] = reports_by_status.get(report.status, 0) + 1

    unresolved_statuses = {"reported", "verified", "assigned", "in_progress"}
    return OperationsSummary(
        total_reports=len(reports),
        unresolved_reports=sum(report.status in unresolved_statuses for report in reports),
        critical_reports=sum(
            report.priority == "critical" and report.status in unresolved_statuses
            for report in reports
        ),
        reports_by_status=reports_by_status,
    )


def build_technician_queue(
    reports: list[ReportSnapshot],
    technician_id: int,
) -> TechnicianQueue:
    active_assignment_statuses = {"assigned", "accepted", "in_progress"}
    matching_reports = [
        report
        for report in reports
        if report.assignment
        and report.assignment.technician.id == technician_id
        and report.assignment.status in active_assignment_statuses
    ]
    technician = (
        matching_reports[0].assignment.technician
        if matching_reports
        else None
    )
    items = [
        QueueItem(
            id=report.id,
            area=report.area,
            description=report.description,
            priority=report.priority,
            report_status=report.status,
            assignment_status=report.assignment.status,
            created_at=report.created_at,
            updated_at=report.updated_at,
        )
        for report in matching_reports
    ]
    return TechnicianQueue(
        technician_id=technician_id,
        technician=technician,
        total=len(items),
        items=items,
    )


def build_public_outages(reports: list[ReportSnapshot]) -> list[PublicOutage]:
    active_statuses = {"reported", "verified", "assigned", "in_progress"}
    return [
        PublicOutage(
            id=report.id,
            area=report.area,
            priority=report.priority,
            status=report.status,
            created_at=report.created_at,
            updated_at=report.updated_at,
            resolved_at=report.resolved_at,
        )
        for report in reports
        if report.status in active_statuses
    ]
