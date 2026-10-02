"""FastAPI route declarations for the task resource."""

from typing import Annotated

import aiosqlite
from fastapi import APIRouter, Depends, HTTPException, Response, status

from .database import get_db
from .repository import create_task, delete_task, get_task, list_tasks, update_task
from .schemas import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])
Database = Annotated[aiosqlite.Connection, Depends(get_db)]


@router.get("/", response_model=list[TaskRead])
async def read_tasks(database: Database) -> list[TaskRead]:
    """Return tasks using an async database dependency."""

    return await list_tasks(database)


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    payload: TaskCreate,
    database: Database,
) -> TaskRead:
    """Validate a request body, persist it, and return the typed response."""

    return await create_task(database, payload)


@router.get("/{task_id}", response_model=TaskRead)
async def read_task(task_id: int, database: Database) -> TaskRead:
    """Read one task; FastAPI validates the integer path parameter."""

    task = await get_task(database, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def patch_task(
    task_id: int,
    payload: TaskUpdate,
    database: Database,
) -> TaskRead:
    """Partially update a task using only fields supplied by the client."""

    task = await update_task(database, task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(task_id: int, database: Database) -> Response:
    """Delete a task and return the HTTP 204 no-content status."""

    if not await delete_task(database, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
