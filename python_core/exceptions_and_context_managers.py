"""Lesson 3: Exception Handling and Context Managers.

===============================================================================
THEORY CONCEPT 1: EXCEPTION HANDLING (try / except / else / finally)
===============================================================================
In web applications (Django, Flask, FastAPI), errors happen frequently:
- A user submits bad data (e.g. string instead of number)
- A database connection drops
- A requested record is not found in the database

If an exception is unhandled, Python crashes the whole request/server!
Exception handling allows us to catch errors gracefully, return friendly
HTTP error responses (like 400 Bad Request or 404 Not Found), and clean up
resources safely.

The 4 Blocks:
  1. `try`: Code that might raise an error.
  2. `except`: Code that runs ONLY if a specific error occurs.
  3. `else`: Code that runs ONLY if NO error occurs in the try block.
  4. `finally`: Code that ALWAYS runs, regardless of whether an error occurred.

===============================================================================
THEORY CONCEPT 2: CUSTOM EXCEPTIONS
===============================================================================
Python has built-in errors (ValueError, TypeError, KeyError). In web backend
dev, we create our own Custom Exception classes inheriting from `Exception`
(e.g., UserNotFoundError, InvalidPermissionError) to clearly communicate what
went wrong in our application logic.

===============================================================================
THEORY CONCEPT 3: CONTEXT MANAGERS (`with` statement)
===============================================================================
Context Managers handle setup and tear-down of resources automatically.
Example: Opening a file or connecting to a database.
Without `with`: If an error occurs while writing to a file, the file stays open in memory!
With `with`: Python guarantees `__exit__` runs to close the file/connection even if errors occur.
"""

from typing import Any


class DatabaseValidationError(Exception):
    """Custom exception raised when database payload validation fails.

    Inheriting from Python's base `Exception` class allows this custom error
    to be caught using `except DatabaseValidationError:`.
    """
    def __init__(self, message: str, error_code: int = 400):
        super().__init__(message)  # Call base Exception constructor
        self.message = message
        self.error_code = error_code


def safe_divide(numerator: float, denominator: float) -> dict[str, Any]:
    """Demonstrate the try / except / else / finally structure with comments."""

    result = None
    status = ""
    cleaned_up = False

    try:
        # 1. TRY: Execute code that might fail (division by zero)
        result = numerator / denominator
    except ZeroDivisionError as err:
        # 2. EXCEPT: Catches ZeroDivisionError specifically
        status = "Error: Cannot divide by zero"
    else:
        # 3. ELSE: Runs ONLY if try block succeeded without any exception
        status = f"Success: Result is {result}"
    finally:
        # 4. FINALLY: Always executes (ideal for cleanup like closing DB connections)
        cleaned_up = True

    return {
        "result": result,
        "status": status,
        "cleaned_up": cleaned_up
    }


def validate_user_age(age: int) -> str:
    """Demonstrate raising a custom exception when validation fails."""
    if age < 0:
        # `raise` triggers an exception manually
        raise DatabaseValidationError("Age cannot be negative!", error_code=400)
    if age < 18:
        return "Minor"
    return "Adult"


class DummyDatabaseConnection:
    """A custom Context Manager implementing __enter__ and __exit__.

    When used with `with DummyDatabaseConnection() as db:`, Python automatically:
    1. Calls `__enter__()` before entering the block.
    2. Calls `__exit__()` when leaving the block (even if an exception was raised!).
    """
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.is_connected = False

    def __enter__(self):
        # Setup phase
        self.is_connected = True
        return self  # The object assigned to `as db`

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Teardown phase: Always disconnects
        self.is_connected = False
        # Returning False allows any exception inside the block to propagate normally.
        return False
