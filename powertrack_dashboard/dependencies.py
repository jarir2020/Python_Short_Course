"""Dependency lookup for the Flask dashboard."""

from flask import current_app

from .repositories import FastAPIOperationsClient


def get_operations_client() -> FastAPIOperationsClient:
    """Return the configured client, or a test replacement if supplied."""

    configured_client = current_app.config.get("OPERATIONS_CLIENT")
    if configured_client is not None:
        return configured_client
    return FastAPIOperationsClient(
        base_url=current_app.config["FASTAPI_BASE_URL"],
        timeout_seconds=current_app.config["UPSTREAM_TIMEOUT_SECONDS"],
    )
