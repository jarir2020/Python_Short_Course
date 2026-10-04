"""Pydantic models for upstream snapshots and public responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserSummary(BaseModel):
    """The safe subset of a Django user needed by operations screens."""

    model_config = ConfigDict(extra="ignore")

    id: int
    username: str
    role: str
    area: str = ""


class ProgressSnapshot(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    technician: UserSummary
    message: str
    status: str
    created_at: datetime


class AssignmentSnapshot(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    technician: UserSummary
    assigned_by: UserSummary
    assigned_at: datetime
    updated_at: datetime
    status: str
    notes: str = ""


class ReportSnapshot(BaseModel):
    """Internal representation of the Django report response."""

    model_config = ConfigDict(extra="ignore")

    id: int
    area: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None
    customer: UserSummary
    assignment: AssignmentSnapshot | None = None
    progress_updates: list[ProgressSnapshot] = Field(default_factory=list)


class OperationsSummary(BaseModel):
    total_reports: int
    unresolved_reports: int
    critical_reports: int
    reports_by_status: dict[str, int]


class QueueItem(BaseModel):
    """The compact report shape useful to a technician queue."""

    id: int
    area: str
    description: str
    priority: str
    report_status: str
    assignment_status: str
    created_at: datetime
    updated_at: datetime


class TechnicianQueue(BaseModel):
    technician_id: int
    technician: UserSummary | None = None
    total: int
    items: list[QueueItem]


class PublicOutage(BaseModel):
    """Safe public status data; customer details stay private."""

    id: int
    area: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None
