"""Application services: business use-cases between routes and persistence.

The route layer should mainly translate HTTP concepts (URLs, status codes, and
headers). A service layer gives the business operation a home that can also be
called from a CLI, a background job, or another transport later.
"""

import aiosqlite

from .repository import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)
from .schemas import TaskCreate, TaskRead, TaskUpdate


class TaskService:
    """Coordinate task use-cases for one request-scoped database connection."""

    def __init__(self, database: aiosqlite.Connection):
        self.database = database

    async def list_for_owner(self, owner_id: int) -> list[TaskRead]:
        return await list_tasks(self.database, owner_id)

    async def create_for_owner(
        self,
        owner_id: int,
        payload: TaskCreate,
    ) -> TaskRead:
        return await create_task(self.database, owner_id, payload)

    async def get_for_owner(
        self,
        task_id: int,
        owner_id: int,
    ) -> TaskRead | None:
        return await get_task(self.database, task_id, owner_id)

    async def update_for_owner(
        self,
        task_id: int,
        owner_id: int,
        payload: TaskUpdate,
    ) -> TaskRead | None:
        return await update_task(self.database, task_id, owner_id, payload)

    async def delete_for_owner(self, task_id: int, owner_id: int) -> bool:
        return await delete_task(self.database, task_id, owner_id)
