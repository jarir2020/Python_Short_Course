import pytest


@pytest.fixture
def anyio_backend() -> str:
    """Run async API tests with the asyncio backend used by the project."""

    return "asyncio"
