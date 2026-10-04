"""Tests use a fake FastAPI client to isolate Flask from network I/O."""

from powertrack_dashboard import create_app
from powertrack_dashboard.repositories import FastAPIUnavailableError


class FakeOperationsClient:
    def __init__(self, outages=None, error=None):
        self.outages = outages if outages is not None else [
            {
                "id": 1,
                "area": "North Road",
                "priority": "critical",
                "status": "in_progress",
                "created_at": "2026-10-04T10:00:00Z",
                "updated_at": "2026-10-04T11:00:00Z",
                "resolved_at": None,
            }
        ]
        self.error = error

    def list_public_outages(self):
        if self.error:
            raise self.error
        return self.outages


def test_dashboard_renders_safe_public_outage_data():
    app = create_app(
        {
            "TESTING": True,
            "OPERATIONS_CLIENT": FakeOperationsClient(),
        }
    )

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200
    assert b"North Road" in response.data
    assert b"Critical" in response.data
    assert b"customer" not in response.data.lower()


def test_json_status_endpoint_returns_validated_data():
    app = create_app(
        {
            "TESTING": True,
            "OPERATIONS_CLIENT": FakeOperationsClient(),
        }
    )

    with app.test_client() as client:
        response = client.get("/api/status")

    assert response.status_code == 200
    assert response.get_json()[0]["area"] == "North Road"


def test_dashboard_shows_dependency_error_without_leaking_upstream_details():
    app = create_app(
        {
            "TESTING": True,
            "OPERATIONS_CLIENT": FakeOperationsClient(
                error=FastAPIUnavailableError("private upstream detail")
            ),
        }
    )

    with app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 503
    assert b"temporarily unavailable" in response.data
    assert b"private upstream detail" not in response.data


def test_health_is_a_liveness_check():
    app = create_app({"TESTING": True})

    with app.test_client() as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "framework": "flask",
        "service": "powertrack-dashboard",
    }
