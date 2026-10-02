# Phase 6: Security, Testing, Deployment, and Capstone

## Authentication flow

```text
username + password -> POST /api/auth/token -> short-lived signed JWT
JWT in Authorization: Bearer ... -> OAuth2PasswordBearer -> current user
```

Passwords are hashed with Argon2 through `pwdlib`; plaintext passwords are not
stored or returned. JWTs are signed, not encrypted, so sensitive information
must not be placed in their payload. The secret key belongs in an environment
variable and must be rotated through a planned operational process.

## Authorization and ownership

Authentication answers “who are you?” Authorization answers “may you access
this resource?” Every task query includes the authenticated user's `owner_id`,
so a valid token for one user cannot retrieve another user's task.

## Security boundaries in this lesson

The capstone adds explicit CORS origins, security response headers, input
validation, parameterized SQL, expiring JWTs, and a small in-memory login rate
limiter. The limiter is intentionally labeled as a teaching implementation: a
multi-worker deployment needs a shared store such as Redis, and production
systems should also add monitoring, refresh-token strategy, account lockout or
risk controls, TLS, secret management, and a security review.

## WSGI versus ASGI

* Django and Flask expose WSGI entry points for synchronous deployment.
* FastAPI exposes an ASGI application and is commonly served by Uvicorn or
  Gunicorn with `UvicornWorker`.
* The development servers are for local work; production needs a proper server
  and deployment configuration.

## Run the capstone

```bash
source .venv/bin/activate
python -m capstone_api.demo
uvicorn capstone_api.main:app --reload
```

Production-style examples:

```bash
gunicorn -c gunicorn.conf.py capstone_api.main:app
CAPSTONE_SECRET_KEY='use-a-long-random-secret' docker compose up --build
```

Run security and regression tests with:

```bash
pytest
python manage.py test
```
