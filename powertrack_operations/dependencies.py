"""FastAPI dependency providers for the PowerTrack integration."""

from typing import Annotated

from fastapi import Depends

from .repositories import DjangoOperationsClient


def get_django_client() -> DjangoOperationsClient:
    """Build one configured repository for the current request."""

    return DjangoOperationsClient()


DjangoClientDependency = Annotated[
    DjangoOperationsClient,
    Depends(get_django_client),
]
