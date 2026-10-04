"""Environment-based settings for the Flask dashboard."""

import os


FASTAPI_BASE_URL = os.environ.get(
    "POWERTRACK_FASTAPI_BASE_URL",
    "http://127.0.0.1:8001",
)
UPSTREAM_TIMEOUT_SECONDS = float(
    os.environ.get("POWERTRACK_FASTAPI_TIMEOUT_SECONDS", "5")
)
