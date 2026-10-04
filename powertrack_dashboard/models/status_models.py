"""Validated data received from FastAPI's public status endpoint."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PublicOutage(BaseModel):
    """The small public contract rendered by the dashboard."""

    model_config = ConfigDict(extra="ignore")

    id: int
    area: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None
