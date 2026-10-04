# Phase 4: FastAPI and Pydantic

## Request flow

```text
HTTP request -> route registration -> controller -> dependencies
             -> service -> async repository -> response model -> JSON response
```

FastAPI reads Python type annotations to understand path parameters, request
bodies, dependencies, and response schemas. Pydantic validates incoming data;
the response model also documents and filters outgoing data.

## Dependency injection

`Depends(get_db)` tells FastAPI to call `get_db`, pass its result into the route,
and close the yielded database connection after the request. Tests can replace
that dependency with a temporary database through
`app.dependency_overrides`, which keeps the application code independent from
test storage.

## Async

`async def` and `await` allow the endpoint to pause while SQLite performs I/O,
so the event loop can serve other work. Async does not make CPU-heavy code
faster; it helps when work spends time waiting on I/O.

## Run the service

```bash
source .venv/bin/activate
python -m fastapi_project.demo
uvicorn fastapi_project.main:app --reload
```

FastAPI publishes interactive documentation at `/docs`, alternative ReDoc
documentation at `/redoc`, and the raw schema at `/openapi.json`.

Run all tests with:

```bash
pytest
```

## MVC-style mapping

The route functions are controllers: they translate HTTP input and status codes. `services/task_service.py` contains use-cases, `repositories/task_repository.py` contains async SQLite statements, and `models/task_models.py` contains validated request and response models. This keeps FastAPI dependency injection visible without hiding the database work.
