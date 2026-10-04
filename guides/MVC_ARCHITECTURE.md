# MVC-style architecture across the projects

The frameworks use different names, but the responsibility flow is the same:

```text
HTTP request
    -> controller (routing and HTTP status codes)
    -> service (business rules and use-cases)
    -> model/repository (domain data and database access)
    -> controller
    -> HTTP response
```

## Framework mapping

| Project | Controller | Model/data layer | View/response layer |
| --- | --- | --- | --- |
| Django | `tasks/controllers/task_controller.py` ViewSet | `tasks/models/task_model.py` and Django ORM | `tasks/serializers/task_serializer.py` |
| FastAPI | `controllers/task_controller.py` | `models/` + `services/` + `repositories/` | `routes/task_routes.py` registers responses |
| Flask | `controllers/task_controller.py` | `models/` + `services/` + `repositories/` | `routes/task_routes.py` registers JSON responses |
| Capstone | `controllers/` | `models/` + `services/` + `repositories/` | `routes/` registers responses |

## Folder layout

```text
project/
  config/
  models/
  controllers/
  routes/
  services/
  repositories/
  tests/
```

Django calls its pattern MVT: the ViewSet acts like a controller, the model
owns persistence, and serializers produce the API representation. Flask and
FastAPI are less opinionated, so the folders make the separation explicit.

## Why keep layers separate?

* Controllers know HTTP, not SQL.
* Services express business operations and can be reused by a CLI or job.
* Repositories contain database statements and parameter binding.
* Models and schemas describe data rather than request flow.
* Tests can exercise a service or repository without opening a web server.

This is not a rule that every small script needs five files. The separation is
useful here because the repository is teaching how a project grows from a
single route into a maintainable backend.

## Run the examples

```bash
source .venv/bin/activate
python -m fastapi_project.demo
python -m flask_project.demo
pytest -q
```
