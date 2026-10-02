"""Flask application factory for the Phase 5 learning service."""

from __future__ import annotations

import os
from time import perf_counter
from uuid import uuid4

from flask import Flask, g, jsonify, request

from .db import init_app, init_db
from .tasks import TaskValidationError, task_api


def create_app(test_config: dict[str, object] | None = None) -> Flask:
    """Create and configure a Flask application instance.

    The factory makes configuration explicit and lets tests create isolated
    applications with a temporary database instead of sharing global state.
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="phase-5-learning-only-change-before-production",
        DATABASE=os.path.join(app.instance_path, "flask.sqlite3"),
    )

    if test_config is None:
        # A local instance/config.py can override defaults without being part
        # of the source package. Tests pass a dictionary instead.
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    init_app(app)
    app.register_blueprint(task_api, url_prefix="/api")

    with app.app_context():
        # CREATE TABLE IF NOT EXISTS makes the demo immediately runnable while
        # keeping repeated factory creation safe.
        init_db()

    @app.before_request
    def start_request() -> None:
        """Store request-scoped data before a view function runs."""

        g.request_started = perf_counter()
        g.request_id = request.headers.get("X-Request-ID", str(uuid4()))

    @app.after_request
    def finish_request(response):
        """Add observability headers after the view has produced a response."""

        elapsed_ms = (perf_counter() - g.request_started) * 1000
        response.headers["X-Request-ID"] = g.request_id
        response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.2f}"
        return response

    @app.teardown_request
    def teardown_request(error: BaseException | None) -> None:
        """Run after request dispatch, even when a view raises an error."""

        if error is not None:
            app.logger.debug("Request %s ended with %s", g.get("request_id"), error)

    @app.errorhandler(TaskValidationError)
    def handle_validation_error(error: TaskValidationError):
        return jsonify(error="validation_error", message=str(error)), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify(error="not_found", message="Resource not found"), 404

    return app
