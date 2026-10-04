"""URL registration for authentication controllers."""

from fastapi import APIRouter

from ..controllers.auth_controller import login_for_access_token, read_current_user, register
from ..models import Token, UserRead


auth_router = APIRouter(prefix="/auth", tags=["auth"])

auth_router.add_api_route(
    "/register",
    register,
    methods=["POST"],
    response_model=UserRead,
    status_code=201,
)
auth_router.add_api_route(
    "/token",
    login_for_access_token,
    methods=["POST"],
    response_model=Token,
)
auth_router.add_api_route(
    "/me",
    read_current_user,
    methods=["GET"],
    response_model=UserRead,
)
