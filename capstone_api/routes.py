"""Authentication and owner-scoped task routes."""

from typing import Annotated

import aiosqlite
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import CurrentUser, Database, SettingsDependency, TaskServiceDependency
from .repository import create_user, find_user
from .schemas import TaskCreate, TaskRead, TaskUpdate, Token, UserCreate, UserRead
from .security import create_access_token, hash_password, verify_password


auth_router = APIRouter(prefix="/auth", tags=["auth"])
task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@auth_router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: UserCreate, database: Database) -> UserRead:
    """Create a user while storing only an Argon2 password hash."""

    if await find_user(database, payload.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    return await create_user(database, payload.username, hash_password(payload.password))


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    database: Database,
    settings: SettingsDependency,
) -> Token:
    """Implement OAuth2's password flow and return a short-lived bearer JWT."""

    user = await find_user(database, form_data.username.strip().lower())
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(
        access_token=create_access_token(user.username, settings),
        token_type="bearer",
    )


@auth_router.get("/me", response_model=UserRead)
async def read_current_user(current_user: CurrentUser) -> UserRead:
    return current_user


@task_router.get("/", response_model=list[TaskRead])
async def read_tasks(
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> list[TaskRead]:
    return await task_service.list_for_owner(current_user.id)


@task_router.post("/", response_model=TaskRead, status_code=201)
async def create_owned_task(
    payload: TaskCreate,
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> TaskRead:
    return await task_service.create_for_owner(current_user.id, payload)


@task_router.get("/{task_id}", response_model=TaskRead)
async def read_owned_task(
    task_id: int,
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> TaskRead:
    task = await task_service.get_for_owner(task_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.patch("/{task_id}", response_model=TaskRead)
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


@task_router.delete("/{task_id}", status_code=204)
async def delete_owned_task(
    task_id: int,
    task_service: TaskServiceDependency,
    current_user: CurrentUser,
) -> Response:
    if not await task_service.delete_for_owner(task_id, current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
