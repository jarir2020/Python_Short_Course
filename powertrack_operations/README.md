# PowerTrack Operations API

This is Stage 2 of `Plan2.md`. It is a small FastAPI read-only service that
calls the PowerTrack Django API over HTTP.

```text
FastAPI route
  -> controller
  -> operation service
  -> Django HTTP repository
  -> Django /api/reports/ endpoint
```

FastAPI does not import Django models and does not open
`powertrack.sqlite3`. That boundary matters: Django remains responsible for
authentication, permissions, workflow transitions, and writes.

## Endpoints

```text
GET /api/operations/summary
GET /api/operations/technicians/<id>/queue
GET /api/public/outages
GET /api/health
```

The first two operations endpoints use a Django admin/service token configured
outside the repository through `POWERTRACK_DJANGO_TOKEN`. The public endpoint
is public to its callers, but FastAPI still uses that internal credential to
read the protected Django report list. It returns only safe status fields and
omits customer names and descriptions.

## Run locally

Start Django first:

```bash
./.venv/bin/python power_outage_project/manage.py runserver 127.0.0.1:8000
```

In another terminal, configure the Django base URL and an operations token
outside the repository, then run FastAPI:

```bash
export POWERTRACK_DJANGO_BASE_URL=http://127.0.0.1:8000
export POWERTRACK_DJANGO_TOKEN=<managed-django-service-token>
./.venv/bin/uvicorn powertrack_operations.main:app --reload --port 8001
```

The placeholder notation above means the value must come from your local
secret manager or shell environment; it is not a value to commit.

## Testing idea

The tests replace the HTTP repository with a fake client. This keeps tests
fast and deterministic while still exercising the FastAPI route, controller,
service calculations, response models, and failure mapping. A separate
deployment check can verify the real Django-to-FastAPI connection.
