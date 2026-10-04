"""Environment-backed settings for the capstone service."""

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


DEFAULT_SECRET_KEY = "change-this-development-secret-please"


@dataclass(frozen=True)
class Settings:
    """Configuration that can be replaced with a test dependency."""

    secret_key: str
    database_path: Path
    algorithm: str = "HS256"
    access_token_minutes: int = 30
    cors_origins: tuple[str, ...] = ("http://localhost:3000",)
    rate_limit_requests: int = 10
    rate_limit_window_seconds: int = 60


@lru_cache
def get_settings() -> Settings:
    """Load configuration once per process; secrets come from the environment."""

    environment = os.getenv("CAPSTONE_ENV", "development")
    secret_key = os.getenv("CAPSTONE_SECRET_KEY", DEFAULT_SECRET_KEY)
    if environment == "production" and secret_key == DEFAULT_SECRET_KEY:
        raise RuntimeError("CAPSTONE_SECRET_KEY must be set in production")

    raw_origins = os.getenv("CAPSTONE_CORS_ORIGINS", "http://localhost:3000")
    cors_origins = tuple(origin.strip() for origin in raw_origins.split(",") if origin.strip())
    database_path = Path(
        os.getenv(
            "CAPSTONE_DB_PATH",
            str(Path(__file__).resolve().parent / "capstone.sqlite3"),
        )
    )

    return Settings(
        secret_key=secret_key,
        database_path=database_path,
        cors_origins=cors_origins,
    )
