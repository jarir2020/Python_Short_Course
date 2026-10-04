"""URL registration for the Flask dashboard."""

from flask import Blueprint

from ..controllers import dashboard, health, status_json


status_pages = Blueprint("status_pages", __name__)

status_pages.add_url_rule("/", view_func=dashboard, methods=["GET"])
status_pages.add_url_rule("/api/status", view_func=status_json, methods=["GET"])
status_pages.add_url_rule("/api/health", view_func=health, methods=["GET"])
