"""Lesson 5: Modules, Packages, Virtual Environments, and Execution Context.

===============================================================================
THEORY CONCEPT 1: MODULES vs PACKAGES
===============================================================================
- MODULE: Any single `.py` file containing Python code (e.g. `references.py`).
- PACKAGE: A directory containing multiple modules and an `__init__.py` file.
  The `__init__.py` marks the directory as an importable Python package.

===============================================================================
THEORY CONCEPT 2: THE `if __name__ == "__main__":` GUARD
===============================================================================
Every Python file has a built-in variable named `__name__`.
1. When you run a script DIRECTLY (`python3 script.py`):
   Python sets `__name__ = "__main__"`.
2. When a script is IMPORTED by another module (`import script`):
   Python sets `__name__ = "script"` (the module's file name).

Why is this useful?
It allows a file to serve dual purposes:
- As an importable module containing reusable functions/classes.
- As a standalone script that runs test code ONLY when executed directly!

===============================================================================
THEORY CONCEPT 3: VIRTUAL ENVIRONMENTS & PIP
===============================================================================
What is a Virtual Environment (`venv`)?
In Python, different projects might require different versions of libraries
(e.g., Django 4.2 vs Django 5.0).
A virtual environment creates an isolated folder containing a specific Python
binary and pip package installation directory for one specific project.

Key Commands:
1. Create venv:    `python3 -m venv .venv`
2. Activate venv:  `source .venv/bin/activate` (Linux/macOS)
3. Install package:`pip install django fastapi flask`
4. Export deps:    `pip freeze > requirements.txt`
5. Install deps:   `pip install -r requirements.txt`
"""

def explain_module_imports() -> dict[str, str]:
    """Return key definitions for Python code organization."""
    return {
        "module": "A single .py file containing runnable Python code and definitions.",
        "package": "A directory containing an __init__.py file and multiple modules.",
        "venv": "An isolated Python environment for managing project-specific packages.",
        "pip": "Python's standard package manager used to install third-party libraries.",
    }


if __name__ == "__main__":
    print("This file was executed directly! __name__ is:", __name__)
    print(explain_module_imports())
