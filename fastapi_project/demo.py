"""Run a small in-process demonstration of the Phase 4 API."""

import asyncio
from pprint import pprint

import httpx

from .database import initialize_database
from .main import app


async def main() -> None:
    """Call the ASGI application asynchronously without opening a port."""

    await initialize_database()

    # ASGITransport sends requests directly to the application. Uvicorn is
    # needed only when you want to expose the same app on a network port.
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        health_response = await client.get("/api/health")
        create_response = await client.post(
            "/api/tasks/",
            json={"title": "Learn dependency injection"},
        )
        list_response = await client.get("/api/tasks/")

    pprint({"health": health_response.json()})
    pprint({"created": create_response.json()})
    pprint({"tasks": list_response.json()})


if __name__ == "__main__":
    asyncio.run(main())
