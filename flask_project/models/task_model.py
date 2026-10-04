"""Domain models for the Flask task application.

Flask does not require an ORM. This small dataclass is the model-layer object
that keeps database rows from leaking directly into controller code.
"""

from dataclasses import dataclass
import sqlite3


@dataclass(frozen=True)
class Task:
    """A task as understood by the application, independent of HTTP."""

    id: int
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Task":
        """Translate one SQLite row into a domain model."""

        return cls(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict[str, object]:
        """Create the JSON-safe representation used by the controller."""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
