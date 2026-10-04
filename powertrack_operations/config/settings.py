"""Environment-based settings for the FastAPI integration service."""

import os


# The FastAPI service does not share Django's database. It calls this URL over
# HTTP so Django remains the single source of truth for business data.
DJANGO_BASE_URL = os.environ.get(
    "POWERTRACK_DJANGO_BASE_URL",
    "http://127.0.0.1:8000",
)

# Keep the token outside the repository. It should belong to a controlled
# Django admin/service account and should never be printed by this service.
DJANGO_OPERATIONS_TOKEN = os.environ.get("POWERTRACK_DJANGO_TOKEN")
UPSTREAM_TIMEOUT_SECONDS = float(
    os.environ.get("POWERTRACK_UPSTREAM_TIMEOUT_SECONDS", "5")
)
