import pytest

from flask_project import create_app


@pytest.fixture()
def app(tmp_path):
    """Create an isolated Flask application for each test."""

    return create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


def test_application_factory_and_health_hooks(client):
    response = client.get("/api/health", headers={"X-Request-ID": "test-id"})

    assert response.status_code == 200
    assert response.get_json() == {"framework": "flask", "status": "ok"}
    assert response.headers["X-Request-ID"] == "test-id"
    assert float(response.headers["X-Process-Time-Ms"]) >= 0


def test_blueprint_crud_routes(client):
    created = client.post(
        "/api/tasks",
        json={"title": "  Learn Flask  ", "description": "Use a factory"},
    )

    assert created.status_code == 201
    task = created.get_json()
    assert task["title"] == "Learn Flask"
    assert task["status"] == "todo"

    task_id = task["id"]
    listed = client.get("/api/tasks")
    assert [item["id"] for item in listed.get_json()] == [task_id]

    updated = client.patch(f"/api/tasks/{task_id}", json={"status": "done"})
    assert updated.status_code == 200
    assert updated.get_json()["status"] == "done"

    deleted = client.delete(f"/api/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404


def test_validation_error_is_json(client):
    response = client.post("/api/tasks", json={"title": "   "})

    assert response.status_code == 400
    assert response.get_json()["error"] == "validation_error"


def test_unknown_route_uses_json_error_handler(client):
    response = client.get("/api/does-not-exist")

    assert response.status_code == 404
    assert response.get_json()["error"] == "not_found"
