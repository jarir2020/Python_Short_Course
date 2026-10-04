#!/usr/bin/env python
"""Command-line entry point for the PowerTrack Django project."""

import os
import sys
from pathlib import Path


def main() -> None:
    """Run Django's management commands using this project's settings."""

    # Test discovery uses the current directory. Moving to this project folder
    # prevents Django from accidentally collecting tests from sibling course
    # projects when this command is called from the repository root.
    os.chdir(Path(__file__).resolve().parent)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
