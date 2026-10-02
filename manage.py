#!/usr/bin/env python
"""Django's command-line entry point for the Phase 3 project."""

import os
import sys


def main() -> None:
    """Run a Django management command."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.config.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
