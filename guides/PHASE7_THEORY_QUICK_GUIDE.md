# Phase 7: Production Architecture and Observability

Phase 6 made the API secure. Phase 7 asks a production question: how do we
understand and operate the service after it is running?

## Request path and layers

```text
client
  -> ASGI middleware (request ID, timing, security headers)
  -> route (HTTP translation and status codes)
  -> service (business use-case)
  -> repository (SQL statements)
  -> SQLite database
```

The route should not need to know how a task is stored. `TaskService` is the
application layer; `repository.py` is the persistence layer. This separation
helps unit tests and makes a later database replacement less disruptive.

FastAPI dependencies connect these layers: the database connection is created
per request, and `get_task_service()` receives that connection to build a
service. FastAPI supports dependencies that are callable objects and can be
composed into dependency chains.

## Liveness versus readiness

* `/api/health/live` answers: “Is the process responding?”
* `/api/health/ready` answers: “Can the process reach its database?”

A load balancer can use readiness to stop sending traffic to an instance whose
dependency is unavailable. A process supervisor can use liveness to decide
whether the application itself needs restarting. These checks should stay
cheap and should not expose secrets or full database details.

## Observability basics

The middleware adds:

* `X-Request-ID`: one safe correlation ID for a request and its logs.
* `X-Process-Time`: elapsed application time in seconds.
* a log record containing method, path, status, duration, and request ID.

It deliberately does not log request bodies or authorization headers. In a
larger system, send structured logs and metrics to a central platform and add
distributed tracing such as OpenTelemetry.

## CI quality gates

`.github/workflows/ci.yml` runs the same three local checks on pushes and pull
requests: pytest, Django tests, and bytecode compilation. CI catches broken
imports and regressions before deployment, but a green build is not proof that
the production environment, migrations, secrets, or external dependencies are
correct.

## Run Phase 7

```bash
source .venv/bin/activate
pytest -q
python manage.py test
python -m capstone_api.demo
```

Try the health checks with the development server:

```bash
uvicorn capstone_api.main:app --reload
curl -i http://127.0.0.1:8000/api/health/live
curl -i http://127.0.0.1:8000/api/health/ready
```

## Architecture comparison

The capstone already uses `services/` and `repositories/` layers. Phase 4 and Phase 5 now use the same folder structure, while Django demonstrates the framework-native MVT version. See [guides/MVC_ARCHITECTURE.md](guides/MVC_ARCHITECTURE.md).
