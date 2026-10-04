# PowerTrack

PowerTrack is a small Load Shedding and Power Outage Management System. It is
the next practical project in this course and is intentionally built with
Django and Django REST Framework first.

## Why Django is primary

Django gives this project authentication, migrations, an admin site, ORM
relationships, and a mature request/permission system in one place. FastAPI
and Flask can be added later for focused read-only services, but Django stays
the source of truth for outage data.

## Roles

- Customer: register, submit an outage report, and view their own reports.
- Admin: review reports, change priority, and assign technicians.
- Technician: view assigned reports and record progress until resolution.

## Request path

```text
HTTP route
  -> controller (DRF APIView)
  -> service (workflow rules)
  -> repository (Django ORM)
  -> model (database)
```

The serializer is the boundary that validates incoming JSON and shapes safe
JSON responses. A customer cannot submit a priority, status, or technician
because those fields are controlled by the service workflow.

## Project structure

```text
config/         Django settings, URLs, ASGI, and WSGI
accounts/       custom user, roles, authentication, and account layers
outages/        reports, assignments, progress, and workflow layers
common/         reusable permissions and workflow exceptions
tests/          project-level test documentation
```

The Django test runner conventionally discovers `outages/tests.py`; that file
contains the first workflow tests. The separate `tests/` directory is kept for
future cross-app tests and shared test utilities.

## Run it locally

From the repository root:

```bash
./.venv/bin/python power_outage_project/manage.py check
./.venv/bin/python power_outage_project/manage.py makemigrations
./.venv/bin/python power_outage_project/manage.py migrate
./.venv/bin/python power_outage_project/manage.py test
./.venv/bin/python power_outage_project/manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/`.

## Main endpoints

```text
POST /api/auth/register/       public customer registration
POST /api/auth/login/          token login
GET  /api/auth/me/             current authenticated user
GET  /api/reports/             role-filtered report list
POST /api/reports/             customer creates a report
GET  /api/reports/<id>/        view one permitted report
PATCH /api/reports/<id>/       admin changes priority/status
POST /api/reports/<id>/assign/ admin assigns a technician
GET  /api/reports/<id>/progress/  read progress history
POST /api/reports/<id>/progress/ technician records progress
```

Use the returned token with:

```text
Authorization: Token <token>
```

## Manual workflow

1. Register a customer using `/api/auth/register/`.
2. Create technician and admin users in `/admin/` after creating a superuser.
3. Log in as the customer and create a report.
4. Log in as the admin and assign the report to the technician.
5. Log in as the technician and post `accepted`, `in_progress`, and `resolved`
   progress updates.
6. Log in as the customer and confirm that the report is now resolved.

The automated tests perform this same scenario without requiring a browser.

## Current scope and future integration

This is Stage 1 from `Plan2.md`: Django owns the complete workflow. A later
stage can expose read-only operations summaries through FastAPI, followed by a
small Flask public status page. Those services should call Django APIs rather
than writing directly to Django's database.
