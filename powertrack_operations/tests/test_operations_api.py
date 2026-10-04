"""API tests use a fake repository so they never need a live Django server."""

from collections.abc import AsyncIterator

import httpx
import pytest

from powertrack_operations.dependencies import get_django_client
from powertrack_operations.main import app


REPORTS = [
    {
        "id": 1,
        "customer": {"id": 10, "username": "customer1", "role": "customer", "area": "North Road"},
        "area": "North Road",
        "description": "Transformer is silent.",
        "priority": "critical",
        "status": "in_progress",
        "created_at": "2026-10-04T10:00:00Z",
        "updated_at": "2026-10-04T11:00:00Z",
        "resolved_at": None,
        "assignment": {
            "id": 1,
            "technician": {"id": 20, "username": "technician1", "role": "technician", "area": ""},
            "assigned_by": {"id": 30, "username": "admin1", "role": "admin", "area": ""},
            "assigned_at": "2026-10-04T10:15:00Z",
            "updated_at": "2026-10-04T10:30:00Z",
            "status": "in_progress",
            "notes": "Check the local transformer.",
        },
        "progress_updates": [],
    },
    {
        "id": 2,
        "customer": {"id": 11, "username": "customer2", "role": "customer", "area": "South Road"},
        "area": "South Road",
        "description": "Streetlights are off.",
        "priority": "high",
        "status": "reported",
        "created_at": "2026-10-04T09:00:00Z",
        "updated_at": "2026-10-04T09:00:00Z",
        "resolved_at": None,
        "assignment": None,
        "progress_updates": [],
    },
    {
        "id": 3,
        "customer": {"id": 12, "username": "customer3", "role": "customer", "area": "West Road"},
        "area": "West Road",
        "description": "Power restored.",
        "priority": "medium",
        "status": "resolved",
        "created_at": "2026-10-03T09:00:00Z",
        "updated_at": "2026-10-03T12:00:00Z",
        "resolved_at": "2026-10-03T12:00:00Z",
        "assignment": {
            "id": 3,
            "technician": {"id": 20, "username": "technician1", "role": "technician", "area": ""},
            "assigned_by": {"id": 30, "username": "admin1", "role": "admin", "area": ""},
            "assigned_at": "2026-10-03T09:15:00Z",
            "updated_at": "2026-10-03T12:00:00Z",
            "status": "resolved",
            "notes": "Completed.",
        },
        "progress_updates": [],
    },
]


class FakeDjangoClient:
    def __init__(self, reports=None, error=None):
        self.reports = reports if reports is not None else REPORTS
        self.error = error

    async def list_reports(self):
        if self.error:
            raise self.error
        return self.reports


@pytest.fixture
async def api_client() -> AsyncIterator[httpx.AsyncClient]:
    """Replace the HTTP repository with deterministic in-memory responses."""

    app.dependency_overrides[get_django_client] = lambda: FakeDjangoClient()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_health_identifies_the_operations_service(api_client):
    response = await api_client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["service"] == "powertrack-operations"


@pytest.mark.anyio
async def test_summary_aggregates_reports_from_django(api_client):
    response = await api_client.get("/api/operations/summary")

    assert response.status_code == 200
    assert response.json() == {
        "total_reports": 3,
        "unresolved_reports": 2,
        "critical_reports": 1,
        "reports_by_status": {"in_progress": 1, "reported": 1, "resolved": 1},
    }


@pytest.mark.anyio
async def test_technician_queue_contains_only_active_assignments(api_client):
    response = await api_client.get("/api/operations/technicians/20/queue")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["technician"]["username"] == "technician1"
    assert payload["items"][0]["id"] == 1


@pytest.mark.anyio
async def test_public_endpoint_hides_private_fields_and_resolved_reports(api_client):
    response = await api_client.get("/api/public/outages")

    assert response.status_code == 200
    outages = response.json()
    assert [item["id"] for item in outages] == [1, 2]
    assert "description" not in outages[0]
    assert "customer" not in outages[0]


@pytest.mark.anyio
async def test_upstream_failure_becomes_bad_gateway():
    from powertrack_operations.repositories import DjangoUpstreamError

    app.dependency_overrides[get_django_client] = lambda: FakeDjangoClient(
        error=DjangoUpstreamError("unavailable")
    )
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/operations/summary")
    app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json()["detail"] == "PowerTrack Django integration is unavailable."
