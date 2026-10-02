import pytest


@pytest.fixture
def anyio_backend() -> str:
    """Run AnyIO tests with asyncio; the project lesson is asyncio-based."""

    return "asyncio"
