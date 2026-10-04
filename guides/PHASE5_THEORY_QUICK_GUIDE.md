# Phase 5: Flask and Microframework Architecture

## Why Flask is a microframework

Flask provides the application object, routing, request/response handling, and
extension points. It does not prescribe a project layout, ORM, authentication
system, or admin site the way Django does. That gives you flexibility, but you
must choose and connect more components yourself.

## Application factory

`create_app()` constructs and configures an application. This makes it possible
to create separate instances for development and tests with different database
paths and settings.

## Blueprint and request lifecycle

The task API is registered as a blueprint, which keeps routes modular. For
each request Flask runs the `before_request` hook, dispatches the view, runs
`after_request`, and finally tears down the request/application context. The
example records a request ID and processing time in response headers.

## Database connection lifecycle

`get_db()` stores one SQLite connection in Flask's `g` object. The
`teardown_appcontext` hook closes it automatically. This prevents every route
from opening its own unmanaged connection.

Run the service:

```bash
source .venv/bin/activate
python -m flask_project.demo
flask --app flask_project.wsgi:app run --debug
```

The Phase 5 service uses direct SQLite to keep Flask's core visible. A later
extension lesson can replace it with Flask-SQLAlchemy without changing the
application-factory or blueprint ideas.

## MVC-style mapping

The blueprint functions in `controllers/task_controller.py` are controllers. `services/task_service.py` owns validation and use-cases, `models/task_model.py` contains the domain object, and `repositories/task_repository.py` owns SQL. `tasks.py` remains only as a compatibility export for earlier learner imports.
