"""HTTP repository for the FastAPI public outage endpoint."""

from typing import Any

import requests


class FastAPIUnavailableError(RuntimeError):
    """Raised when the dashboard cannot receive a valid FastAPI response."""


class FastAPIOperationsClient:
    """Small synchronous client used by Flask request handlers."""

    def __init__(self, base_url: str, timeout_seconds: float = 5) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def list_public_outages(self) -> list[dict[str, Any]]:
        try:
            response = requests.get(
                f"{self.base_url}/api/public/outages",
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as error:
            raise FastAPIUnavailableError("FastAPI could not be reached.") from error

        if response.status_code >= 400:
            raise FastAPIUnavailableError(
                f"FastAPI returned HTTP {response.status_code}."
            )

        try:
            payload = response.json()
        except ValueError as error:
            raise FastAPIUnavailableError("FastAPI returned invalid JSON.") from error

        if not isinstance(payload, list):
            raise FastAPIUnavailableError("FastAPI returned an unexpected status shape.")
        return payload
