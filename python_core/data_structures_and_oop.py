"""Lesson 2: Core Data Structures, Functions (*args/**kwargs), and OOP Fundamentals.

This module provides simple, clear Python examples for beginners:
1. Data Structures: Lists, Dictionaries, Sets, Tuples
2. Functions: Positional arguments, Keyword arguments, *args, **kwargs
3. OOP Basics: Classes, attributes, __init__, and methods
"""

def demonstrate_data_structures() -> dict:
    """Show basic operations on lists, dicts, tuples, and sets."""

    # List: ordered, mutable sequence
    fruits = ["apple", "banana"]
    fruits.append("cherry")

    # Tuple: ordered, IMMUTABLE sequence
    coordinates = (10.0, 20.0)

    # Dict: key-value mapping
    user = {"name": "Alice", "role": "Developer"}
    user["email"] = "alice@example.com"

    # Set: unordered collection of UNIQUE elements
    unique_numbers = {1, 2, 2, 3, 3, 3}  # Duplicates automatically removed -> {1, 2, 3}

    return {
        "fruits": fruits,
        "coordinates": coordinates,
        "user_name": user["name"],
        "user": user,
        "unique_numbers": list(unique_numbers)
    }


def calculate_total(*args: float, **kwargs: float) -> float:
    """Demonstrate *args (multiple positional arguments) and **kwargs (keyword arguments).

    *args gathers extra positional arguments into a tuple.
    **kwargs gathers extra named arguments into a dictionary.
    """
    total = sum(args)

    # Add any extra amounts passed as keyword arguments (e.g. tax=5.0, tip=2.0)
    for key, value in kwargs.items():
        total += value

    return total


class SimpleUser:
    """A basic Object-Oriented Programming (OOP) example.

    In Python, 'self' refers to the specific object instance created from the class.
    '__init__' is the constructor method run automatically when a new object is created.
    """

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.is_active = True

    def deactivate(self) -> None:
        """Instance method to update state."""
        self.is_active = False

    def get_info(self) -> str:
        """Return formatted user description."""
        status = "Active" if self.is_active else "Inactive"
        return f"User({self.username}, {self.email}) - {status}"
