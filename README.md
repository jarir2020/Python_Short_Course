# Python, Django, Flask, and FastAPI learning track

The learning order for this repository is documented in [Plan.md](Plan.md).
Phase 1 is intentionally dependency-free and uses only Python's standard
library. It is split into small lessons with runnable examples and tests.

## Run the Phase 1 demo

From the project root:

```bash
python -m python_core.demo
```

Run its tests with:

```bash
python -m unittest discover -s tests -v
```

The code comments explain the theory immediately beside the behavior. The
tests are also examples: each test connects one concept to an observable
result instead of treating the lesson as a collection of definitions.

Current Phase 1 lessons cover syntax and control flow, references and scope,
data structures and OOP, exceptions and context managers, decorators and type
hints, modules and virtual environments, and iterables and generators.

## Run Phase 2

Phase 2 adds a local HTTP and SQLite lab. It uses the `requests` package for HTTP calls and SQLite in memory for SQL practice, so the examples are repeatable without an external service.

```bash
python -m pip install -r requirements.txt
python -m web_backend.demo
```

## Run Phase 3

Phase 3 contains a small authenticated Django REST Framework task API.

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py test
python manage.py runserver
```

See [guides/PHASE3_THEORY_QUICK_GUIDE.md](guides/PHASE3_THEORY_QUICK_GUIDE.md) for the theory map.

## Run Phase 4

Phase 4 contains a typed FastAPI service using Pydantic, async SQLite, dependency injection, and OpenAPI documentation.

```bash
source .venv/bin/activate
python -m fastapi_project.demo
pytest
uvicorn fastapi_project.main:app --reload
```

## Run Phase 5

Phase 5 contains a Flask application factory, blueprint-based task API, SQLite connection lifecycle, request hooks, and JSON error handling.

```bash
source .venv/bin/activate
python -m flask_project.demo
flask --app flask_project.wsgi:app run --debug
```

## Run Phase 6

Phase 6 adds the secured capstone API: OAuth2 password login, Argon2 hashing, JWTs, owner-scoped tasks, security headers, rate limiting, deployment files, and security-focused tests.

```bash
source .venv/bin/activate
python -m capstone_api.demo
pytest
python manage.py test
```

Deployment examples are in [guides/PHASE6_THEORY_QUICK_GUIDE.md](guides/PHASE6_THEORY_QUICK_GUIDE.md).

## Run Phase 7

Phase 7 adds production architecture and observability to the capstone: service/repository layering, request IDs, timing metadata, liveness/readiness checks, and a CI workflow.

```bash
source .venv/bin/activate
pytest -q
python manage.py test
uvicorn capstone_api.main:app --reload
```

Read [guides/PHASE7_THEORY_QUICK_GUIDE.md](guides/PHASE7_THEORY_QUICK_GUIDE.md) for the request path and the theory behind each layer.

# Python_Short_Course

## MVC-style architecture

The framework examples now use the same responsibility flow: controller for HTTP, service for business rules, model or schema for data, and repository for database access. Django uses its native MVT naming, where a ViewSet acts as the controller and serializers shape the API response.

See [guides/MVC_ARCHITECTURE.md](guides/MVC_ARCHITECTURE.md) for the mapping, folder tree, and request diagrams.

The backend packages use explicit `config/`, `models/`, `controllers/`, `routes/`, `services/`, `repositories/`, and `tests/` folders. Django uses the same visible folders while preserving its native MVT terminology.

## PowerTrack practical project

The repository now includes [PowerTrack](power_outage_project/README.md), a
small Django REST Framework project for managing load-shedding and power
outage reports. It demonstrates a custom role-aware user, customer reports,
admin assignment, technician progress updates, workflow rules, and tests.

Run its first stage from the repository root:

```bash
./.venv/bin/python power_outage_project/manage.py migrate
./.venv/bin/python power_outage_project/manage.py test
```

The detailed plan is in [Plan2.md](Plan2.md).

## PowerTrack Stage 2: FastAPI operations service

PowerTrack now also includes a read-only FastAPI service. It calls Django over
HTTP and never opens Django's SQLite database directly.

```bash
./.venv/bin/pytest -q powertrack_operations/tests
./.venv/bin/uvicorn powertrack_operations.main:app --reload --port 8001
```

Configure `POWERTRACK_DJANGO_BASE_URL` and `POWERTRACK_DJANGO_TOKEN` in the
local environment before using the operations endpoints. See
[guides/POWERTRACK_INTEGRATION.md](guides/POWERTRACK_INTEGRATION.md) for the
request path, failure behavior, and scaling tradeoff.

## PowerTrack Stage 3: Flask public dashboard

The Flask dashboard consumes FastAPI's safe public outage response and renders
an HTML status page.

```bash
export POWERTRACK_FASTAPI_BASE_URL=http://127.0.0.1:8001
./.venv/bin/flask --app powertrack_dashboard.wsgi:app run --port 8002
```

Open `http://127.0.0.1:8002/`. The dashboard is read-only and displays a
friendly temporary-unavailable page if FastAPI is down.

## Run and manually test all PowerTrack services

The root `run.sh` starts the services in the correct order, waits for their
health endpoints, and keeps them running for browser/API testing:

```bash
./run.sh
```

Useful alternatives:

```bash
./run.sh smoke   # start services, check them, and stop
./run.sh test    # run pytest, Django tests, and compilation
```

Set `POWERTRACK_DJANGO_TOKEN` in the shell before `./run.sh` if you want the
FastAPI and Flask services to display real Django outage data. Without it, the
services still start and the public data endpoint safely returns `503`.
