"""Business preparation for the public status page."""

from typing import Protocol

from pydantic import ValidationError

from ..models import PublicOutage
from ..repositories import FastAPIUnavailableError


class PublicStatusReader(Protocol):
    def list_public_outages(self) -> list[dict]:
        ...


def list_public_outages(client: PublicStatusReader) -> list[PublicOutage]:
    """Read and validate the upstream public contract."""

    try:
        return [
            PublicOutage.model_validate(item)
            for item in client.list_public_outages()
        ]
    except ValidationError as error:
        raise FastAPIUnavailableError("FastAPI returned invalid outage data.") from error
