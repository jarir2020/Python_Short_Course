"""HTTP repository for reading PowerTrack data from Django."""

from typing import Any

import httpx

from ..config.settings import (
    DJANGO_BASE_URL,
    DJANGO_OPERATIONS_TOKEN,
    UPSTREAM_TIMEOUT_SECONDS,
)


class UpstreamConfigurationError(RuntimeError):
    """Raised when the FastAPI service lacks its Django service token."""


class DjangoUpstreamError(RuntimeError):
    """Raised when Django cannot provide a valid read response."""


class DjangoOperationsClient:
    """Read-only HTTP client for Django's authenticated report API."""

    def __init__(
        self,
        base_url: str = DJANGO_BASE_URL,
        token: str | None = DJANGO_OPERATIONS_TOKEN,
        timeout_seconds: float = UPSTREAM_TIMEOUT_SECONDS,
    ) -> None:
        self.base_url = base_url
        self.token = token
        self.timeout_seconds = timeout_seconds

    async def list_reports(self) -> list[dict[str, Any]]:
        """Fetch all reports visible to the configured Django service user."""

        if not self.token:
            raise UpstreamConfigurationError(
                "POWERTRACK_DJANGO_TOKEN is not configured."
            )

        headers = {"Authorization": f"Token {self.token}"}
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout_seconds,
            ) as client:
                response = await client.get("/api/reports/", headers=headers)
        except httpx.HTTPError as error:
            raise DjangoUpstreamError("Django could not be reached.") from error

        if response.status_code in {401, 403}:
            raise DjangoUpstreamError("Django rejected the operations credentials.")
        if response.status_code >= 400:
            raise DjangoUpstreamError(
                f"Django returned HTTP {response.status_code}."
            )

        try:
            payload = response.json()
        except ValueError as error:
            raise DjangoUpstreamError("Django returned invalid JSON.") from error

        if not isinstance(payload, list):
            raise DjangoUpstreamError("Django returned an unexpected report shape.")
        return payload
