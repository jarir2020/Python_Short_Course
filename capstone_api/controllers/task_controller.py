"""Owner-scoped task controllers for the capstone API."""

from fastapi import HTTPException, Response

from ..dependencies import CurrentUser, TaskServiceDependency
from ..models import TaskCreate, TaskRead, TaskUpdate


async def read_tasks(
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> list[TaskRead]:
    return await task_service.list_for_owner(current_user.id)


async def create_owned_task(
    payload: TaskCreate,
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> TaskRead:
    return await task_service.create_for_owner(current_user.id, payload)


async def read_owned_task(
    task_id: int,
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> TaskRead:
    task = await task_service.get_for_owner(task_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def update_owned_task(
    task_id: int,
    payload: TaskUpdate,
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> TaskRead:
    task = await task_service.update_for_owner(task_id, current_user.id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def delete_owned_task(
    task_id: int,
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> Response:
    if not await task_service.delete_for_owner(task_id, current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
