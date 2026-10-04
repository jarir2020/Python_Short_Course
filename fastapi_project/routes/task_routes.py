"""URL and HTTP-method registration for FastAPI controllers."""

from fastapi import APIRouter, status

from ..controllers.task_controller import (
    create_new_task,
    patch_task,
    read_task,
    read_tasks,
    remove_task,
)
from ..models import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])

# Routes connect URLs to controllers. The controller code remains reusable and
# does not need to know which URL or HTTP verb invoked it.
router.add_api_route("/", read_tasks, methods=["GET"], response_model=list[TaskRead])
router.add_api_route(
    "/",
    create_new_task,
    methods=["POST"],
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
router.add_api_route(
    "/{task_id}",
    read_task,
    methods=["GET"],
    response_model=TaskRead,
)
router.add_api_route(
    "/{task_id}",
    patch_task,
    methods=["PATCH"],
    response_model=TaskRead,
)
router.add_api_route(
    "/{task_id}",
    remove_task,
    methods=["DELETE"],
    status_code=status.HTTP_204_NO_CONTENT,
)
