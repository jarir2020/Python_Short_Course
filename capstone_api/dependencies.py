"""FastAPI dependencies for database access, services, and authenticated users."""

from typing import Annotated

import aiosqlite
import jwt
from fastapi import Depends, HTTPException, status

from .config import Settings, get_settings
from .database import get_db
from .repository import StoredUser, find_user
from .security import decode_access_token, oauth2_scheme
from .services import TaskService


Database = Annotated[aiosqlite.Connection, Depends(get_db)]
SettingsDependency = Annotated[Settings, Depends(get_settings)]


async def get_task_service(database: Database) -> TaskService:
    """Build a service from the request-scoped database dependency."""

    return TaskService(database)


TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    database: Database,
    settings: SettingsDependency,
) -> StoredUser:
    """Validate a bearer token and resolve its subject to a database user."""

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = decode_access_token(token, settings)
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_error from None

    user = await find_user(database, username)
    if user is None:
        raise credentials_error
    return user


CurrentUser = Annotated[StoredUser, Depends(get_current_user)]
