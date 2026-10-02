"""ASGI config for the Phase 3 project."""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.config.settings")

application = get_asgi_application()
