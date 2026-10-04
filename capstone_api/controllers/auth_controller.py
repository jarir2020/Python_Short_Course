"""Authentication controllers for the capstone API."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import CurrentUser, Database, SettingsDependency
from ..models import Token, UserCreate, UserRead
from ..repositories import create_user, find_user
from ..security import create_access_token, hash_password, verify_password


async def register(payload: UserCreate, database: Database) -> UserRead:
    """Create a user while storing only an Argon2 password hash."""

    if await find_user(database, payload.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    return await create_user(database, payload.username, hash_password(payload.password))


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    database: Database,
    settings: SettingsDependency,
) -> Token:
    """Validate credentials and return a short-lived bearer JWT."""

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


async def read_current_user(current_user: CurrentUser) -> UserRead:
    return current_user
