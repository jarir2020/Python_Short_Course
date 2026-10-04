"""FastAPI dependencies that assemble the application's layers."""

from typing import Annotated

import aiosqlite
from fastapi import Depends

from .database import get_db
from .services import TaskService


Database = Annotated[aiosqlite.Connection, Depends(get_db)]


async def get_task_service(database: Database) -> TaskService:
    """Build a service from the request-scoped database connection."""

    return TaskService(database)


# The controller declares this type and FastAPI resolves the dependency chain:
# controller -> service -> database connection.
TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]
