# Agent instructions

## Project purpose

This repository is a beginner-friendly Python backend course. The learner
needs to understand the theory, not only receive working code.

## Before changing code

- Read `Plan.md` and the relevant `guides/PHASE*_THEORY_QUICK_GUIDE.md`.
- Inspect the existing implementation and tests before editing.
- Preserve unrelated user changes and do not delete project files casually.
- Use the project virtual environment at `.venv/bin/python` when available.

## Coding style

- Add concise comments or docstrings when a framework or Python behavior may
  be unfamiliar to a beginner.
- Keep route handling, business logic, and persistence concerns separate.
- Prefer small, deterministic examples and tests over hidden magic.
- Never put passwords, API keys, tokens, or local `.env` values in source,
  documentation, commits, or command output.

## Validation

Run the checks relevant to the change. For backend changes, normally run:

```bash
./.venv/bin/pytest -q
./.venv/bin/python manage.py test
./.venv/bin/python -m compileall -q python_core web_backend django_project fastapi_project flask_project capstone_api tests
```

For deployment changes, also validate the relevant Gunicorn, Docker, or
application import configuration without claiming that local validation is a
live deployment.

## Generated and local files

SQLite databases, Python caches, pytest caches, virtual environments, and
`.env` files are local artifacts. Keep them ignored and do not commit them.

## Documentation

When a phase changes, update the phase guide and `README.md`. Explain the
request path, tradeoffs, and production limitations in plain language.
