"""SQLite connection lifecycle for the Flask application."""

from __future__ import annotations

import sqlite3

import click
from flask import Flask, current_app, g


def get_db() -> sqlite3.Connection:
    """Return the connection associated with the current application context."""

    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error: BaseException | None = None) -> None:
    """Close and remove the request/application-scoped database connection."""

    del error  # The hook receives an error, but closing is the same either way.
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db() -> None:
    """Create the schema from the SQL file packaged with the application."""

    database = get_db()
    with current_app.open_resource("schema.sql") as schema_file:
        database.executescript(schema_file.read().decode("utf-8"))
    database.commit()


def init_app(app: Flask) -> None:
    """Register database teardown and a small ``flask init-db`` command."""

    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command() -> None:
        init_db()
        click.echo("Initialized the database.")
