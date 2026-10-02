"""Pydantic models used as FastAPI request and response schemas."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    """Allowed values for a task's lifecycle state."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Validated JSON body for creating a task."""

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    status: TaskStatus = TaskStatus.TODO

    @field_validator("title")
    @classmethod
    def title_must_contain_text(cls, value: str) -> str:
        """Normalize whitespace and reject a visually empty title."""

        cleaned_title = value.strip()
        if not cleaned_title:
            raise ValueError("title must contain visible text")
        return cleaned_title


class TaskUpdate(BaseModel):
    """Optional fields for a PATCH request.

    ``None`` means a field was not supplied. The repository excludes such
    values, so a PATCH changes only the fields the caller sends.
    """

    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None

    @field_validator("title")
    @classmethod
    def optional_title_must_contain_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned_title = value.strip()
        if not cleaned_title:
            raise ValueError("title must contain visible text")
        return cleaned_title


class TaskRead(BaseModel):
    """Public response model; database-only fields cannot leak accidentally."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """Response schema for the health endpoint."""

    status: str
    framework: str
