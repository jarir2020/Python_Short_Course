"""Application/business services for the Phase 4 task API."""

import aiosqlite

from ..repositories import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)
from ..models import TaskCreate, TaskRead, TaskUpdate


class TaskService:
    """Coordinate task use-cases without knowing HTTP details."""

    def __init__(self, database: aiosqlite.Connection):
        self.database = database

    async def list_all(self) -> list[TaskRead]:
        return await list_tasks(self.database)

    async def create(self, payload: TaskCreate) -> TaskRead:
        return await create_task(self.database, payload)

    async def get(self, task_id: int) -> TaskRead | None:
        return await get_task(self.database, task_id)

    async def update(self, task_id: int, payload: TaskUpdate) -> TaskRead | None:
        return await update_task(self.database, task_id, payload)

    async def delete(self, task_id: int) -> bool:
        return await delete_task(self.database, task_id)
