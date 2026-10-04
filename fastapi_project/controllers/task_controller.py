"""FastAPI controllers: translate HTTP inputs into service calls."""

from fastapi import HTTPException, Response, status

from ..dependencies import TaskServiceDependency
from ..models import TaskCreate, TaskRead, TaskUpdate


async def read_tasks(task_service: TaskServiceDependency) -> list[TaskRead]:
    return await task_service.list_all()


async def create_new_task(
    payload: TaskCreate,
    task_service: TaskServiceDependency,
) -> TaskRead:
    return await task_service.create(payload)


async def read_task(task_id: int, task_service: TaskServiceDependency) -> TaskRead:
    task = await task_service.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def patch_task(
    task_id: int,
    payload: TaskUpdate,
    task_service: TaskServiceDependency,
) -> TaskRead:
    task = await task_service.update(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def remove_task(task_id: int, task_service: TaskServiceDependency) -> Response:
    if not await task_service.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
