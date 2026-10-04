"""Flask public status dashboard for PowerTrack."""

from flask import Flask

from .config.settings import FASTAPI_BASE_URL, UPSTREAM_TIMEOUT_SECONDS
from .routes import status_pages


def create_app(test_config: dict[str, object] | None = None) -> Flask:
    """Create the public dashboard application.

    The application factory makes the upstream client replaceable in tests,
    so tests do not need a running FastAPI process.
    """

    app = Flask(__name__)
    app.config.from_mapping(
        FASTAPI_BASE_URL=FASTAPI_BASE_URL,
        UPSTREAM_TIMEOUT_SECONDS=UPSTREAM_TIMEOUT_SECONDS,
    )
    if test_config is not None:
        app.config.from_mapping(test_config)

    app.register_blueprint(status_pages)
    return app
