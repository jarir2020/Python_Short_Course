"""FastAPI controllers for PowerTrack read-only endpoints."""

from fastapi import HTTPException, status

from ..dependencies import DjangoClientDependency
from ..models import OperationsSummary, PublicOutage, TechnicianQueue
from ..repositories import DjangoUpstreamError, UpstreamConfigurationError
from ..services import (
    build_public_outages,
    build_summary,
    build_technician_queue,
    read_reports,
)


async def _read_reports_or_raise(client):
    try:
        return await read_reports(client)
    except UpstreamConfigurationError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="PowerTrack Django integration is not configured.",
        ) from error
    except DjangoUpstreamError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="PowerTrack Django integration is unavailable.",
        ) from error


async def read_operations_summary(
    client: DjangoClientDependency,
) -> OperationsSummary:
    reports = await _read_reports_or_raise(client)
    return build_summary(reports)


async def read_technician_queue(
    technician_id: int,
    client: DjangoClientDependency,
) -> TechnicianQueue:
    reports = await _read_reports_or_raise(client)
    return build_technician_queue(reports, technician_id)


async def read_public_outages(
    client: DjangoClientDependency,
) -> list[PublicOutage]:
    reports = await _read_reports_or_raise(client)
    return build_public_outages(reports)
