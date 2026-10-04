"""Route registration exports for the capstone API."""

from .auth_routes import auth_router
from .health_routes import health_router
from .task_routes import task_router

__all__ = ["auth_router", "health_router", "task_router"]
