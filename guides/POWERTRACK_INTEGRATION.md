# PowerTrack Stage 2: FastAPI integration

## Why use a second service?

Django is the system of record. FastAPI is useful for focused read-heavy
operations views, but it should not bypass Django's workflow rules by opening
the same SQLite file. The service boundary is an HTTP request:

```text
Operations client
      |
      v
FastAPI route -> controller -> service -> HTTP repository
                                              |
                                              v
                                  Django authenticated API
```

The repository is the only layer that knows the upstream URL and token. The
service layer knows how to calculate summaries and queues, but it does not
know how HTTP transport works. This separation makes the calculations easy to
test with a fake repository.

## Endpoint responsibilities

- `/api/operations/summary` counts all reports and unresolved/critical work.
- `/api/operations/technicians/<id>/queue` returns active assignments for one
  technician. Resolved assignments are excluded.
- `/api/public/outages` returns active public status without customer details
  or report descriptions.

The current implementation reads the complete admin-visible report list and
filters it in FastAPI. That is appropriate for this small learning project.
At larger scale, Django could expose purpose-built filtered query endpoints or
an event-driven read model instead of transferring every report.

## Failure behavior

- Missing `POWERTRACK_DJANGO_TOKEN` returns `503 Service Unavailable` because
  the integration is not configured.
- An unreachable Django service or rejected token returns `502 Bad Gateway`.
- An unexpected Django response shape is treated as an upstream contract
  failure rather than silently returning incomplete data.

These statuses distinguish a caller problem from a dependency problem, which
is important when operating multiple services.

## Stage 3: Flask public dashboard

The Flask application in `powertrack_dashboard/` consumes only FastAPI's safe
`/api/public/outages` response:

```text
Browser -> Flask dashboard -> FastAPI public status -> Django
```

Flask has a separate application factory, HTTP repository, validation service,
controllers, routes, Jinja template, and CSS. It does not import Django models
or access either service's database. The dashboard returns a friendly `503`
page when FastAPI is unavailable, while `/api/health` remains a liveness check
that does not require the upstream service.

This gives each framework a focused responsibility:

- Django owns authentication, writes, and workflow rules.
- FastAPI prepares read-only operations data.
- Flask renders a lightweight public page.
