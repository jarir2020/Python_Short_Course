"""HTTP controllers for the Flask public status dashboard."""

from flask import jsonify, render_template

from ..dependencies import get_operations_client
from ..repositories import FastAPIUnavailableError
from ..services import list_public_outages


def dashboard():
    """Render the browser page with active outage status."""

    try:
        outages = list_public_outages(get_operations_client())
    except FastAPIUnavailableError:
        return (
            render_template(
                "status_dashboard.html",
                outages=[],
                error="The live outage service is temporarily unavailable.",
            ),
            503,
        )
    return render_template("status_dashboard.html", outages=outages, error=None)


def status_json():
    """Provide the same public data for lightweight clients and monitoring."""

    try:
        outages = list_public_outages(get_operations_client())
    except FastAPIUnavailableError:
        return jsonify(error="upstream_unavailable"), 503
    return jsonify([outage.model_dump(mode="json") for outage in outages])


def health():
    """Liveness check; it intentionally does not depend on FastAPI."""

    return jsonify(status="ok", framework="flask", service="powertrack-dashboard")
