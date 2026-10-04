"""WSGI entry point for the PowerTrack public dashboard."""

from . import create_app


app = create_app()
