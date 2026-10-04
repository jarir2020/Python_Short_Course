"""Environment-independent settings for the Phase 4 learning service."""

from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "fastapi.sqlite3"
