"""URL registration for owner-scoped task controllers."""

from fastapi import APIRouter

from ..controllers.task_controller import (
    create_owned_task,
    delete_owned_task,
    read_owned_task,
    read_tasks,
    update_owned_task,
)
from ..models import TaskRead


task_router = APIRouter(prefix="/tasks", tags=["tasks"])

task_router.add_api_route(
    "/",
    read_tasks,
    methods=["GET"],
    response_model=list[TaskRead],
)
task_router.add_api_route(
    "/",
    create_owned_task,
    methods=["POST"],
    response_model=TaskRead,
    status_code=201,
)
task_router.add_api_route(
    "/{task_id}",
    read_owned_task,
    methods=["GET"],
    response_model=TaskRead,
)
task_router.add_api_route(
    "/{task_id}",
    update_owned_task,
    methods=["PATCH"],
    response_model=TaskRead,
)
task_router.add_api_route(
    "/{task_id}",
    delete_owned_task,
    methods=["DELETE"],
    status_code=204,
)
