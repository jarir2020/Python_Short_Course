"""WSGI entry point for a production WSGI server."""

from . import create_app


app = create_app()
