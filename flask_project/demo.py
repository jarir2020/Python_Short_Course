"""Run a small demonstration using Flask's test client."""

from tempfile import TemporaryDirectory

from . import create_app


def main() -> None:
    """Exercise the blueprint routes without opening a network port."""

    with TemporaryDirectory() as directory:
        app = create_app(
            {
                "TESTING": True,
                "DATABASE": f"{directory}/demo.sqlite3",
            }
        )
        with app.test_client() as client:
            print(client.get("/api/health").get_json())
            created = client.post(
                "/api/tasks",
                json={"title": "Learn Flask blueprints"},
            )
            print(created.status_code, created.get_json())
            print(client.get("/api/tasks").get_json())


if __name__ == "__main__":
    main()
