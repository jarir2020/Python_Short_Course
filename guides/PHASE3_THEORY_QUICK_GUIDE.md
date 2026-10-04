# Phase 3: Django and Django REST Framework

## Project versus application

A Django **project** contains configuration for the whole site: settings, root
URLs, and WSGI/ASGI entry points. A Django **application** is a reusable
feature area, such as the `tasks` app in this project.

## Request flow

```text
HTTP request -> URL router -> ViewSet action -> Serializer/model -> response
```

The model describes database structure. The serializer validates incoming data
and converts model instances to JSON-friendly data. The viewset coordinates the
request and response. The router creates conventional URLs for list, create,
retrieve, update, partial update, and delete actions.

## Authentication and ownership

Authentication identifies the user. Permissions decide whether that user may
perform the operation. The task API requires an authenticated user and filters
the queryset by `request.user`, so ownership is enforced on reads as well as on
creation.

The client must not submit its own owner ID. `perform_create()` takes ownership
from the authenticated request, which prevents one user from assigning a new
task to another user.

## Run the project

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py test
python manage.py runserver
```

Useful endpoints:

* `GET /api/health/` — public health check
* `GET /api/tasks/` — authenticated task list
* `POST /api/tasks/` — authenticated task creation
* `GET /api/tasks/<id>/` — authenticated owner-only detail

## MVC and Django MVT

Django calls its MVC-like structure MVT. The `Task` model owns persistence, `TaskViewSet` acts as the controller, and `TaskSerializer` validates and shapes the API representation. The URL router connects HTTP requests to the controller.
