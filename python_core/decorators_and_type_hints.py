"""Lesson 4: Decorators, Type Hints, and Dataclasses.

===============================================================================
THEORY CONCEPT 1: FIRST-CLASS FUNCTIONS & DECORATORS
===============================================================================
In Python, functions are "first-class citizens". This means:
- You can pass a function as an argument into another function.
- You can define a function inside another function (nested function).
- You can return a function from another function.

WHAT IS A DECORATOR?
A decorator is simply a function that takes a function as an argument and returns
a modified "wrapper" function. It allows adding behavior BEFORE or AFTER the original
function executes—without changing the original function's code!

Where will you see decorators in Web Development?
- Django: `@login_required` (checks if user is logged in before running view)
- Flask: `@app.route("/user")` (binds URL route to view function)
- FastAPI: `@app.get("/items")` (registers HTTP GET endpoint)

===============================================================================
THEORY CONCEPT 2: functools.wraps
===============================================================================
When a function is wrapped by a decorator, its metadata (`__name__` and `__doc__`)
gets overwritten by the wrapper function. `functools.wraps` preserves the original
function's name and documentation!

===============================================================================
THEORY CONCEPT 3: TYPE HINTS & DATACLASSES
===============================================================================
Python is dynamically typed, but modern backend development (especially FastAPI &
Pydantic) uses Type Hints (e.g., `def greet(name: str) -> str:`) to:
1. Catch bugs early using linters.
2. Enable automatic data validation & API documentation in FastAPI.

`@dataclass` automatically generates standard methods like `__init__`, `__repr__`,
and `__eq__` for classes that primarily store structured data.
"""

from functools import wraps
from dataclasses import dataclass
from typing import Callable, Optional


def log_execution(func: Callable) -> Callable:
    """A decorator that logs when a function starts and finishes execution.

    `@wraps(func)` copies `func`'s name and docstring to `wrapper`.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG]: Executing '{func.__name__}'...")
        result = func(*args, **kwargs)  # Run the original function
        print(f"[LOG]: '{func.__name__}' completed successfully!")
        return result
    return wrapper


def require_role(required_role: str):
    """A decorator that accepts arguments (a 'decorator factory').

    This simulates backend authorization checks (e.g. checking if user is an 'admin').
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(user_role: str, *args, **kwargs):
            if user_role != required_role:
                raise PermissionError(f"Access denied! Requires role: {required_role}")
            return func(user_role, *args, **kwargs)
        return wrapper
    return decorator


# --- APPLYING DECORATORS ---

@log_execution
def process_payment(amount: float) -> str:
    """Simulate processing a payment transaction."""
    return f"Payment of ${amount:.2f} processed."


@require_role("admin")
def delete_database_record(user_role: str, record_id: int) -> str:
    """Simulate a protected admin action."""
    return f"Record {record_id} deleted by {user_role}."


# --- TYPE HINTS & DATACLASS EXAMPLE ---

@dataclass
class Product:
    """Dataclass representing a store product.

    Python automatically creates __init__(self, id, name, price, description=None).
    """
    id: int
    name: str
    price: float
    description: Optional[str] = None  # Optional[str] means str or None

    def calculate_discounted_price(self, discount_percent: float) -> float:
        """Calculate price after discount."""
        return self.price * (1 - discount_percent / 100)
