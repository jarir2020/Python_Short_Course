"""WSGI config for the Phase 3 project."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.config.settings")

application = get_wsgi_application()
