"""Examples for Python's names, objects, mutability, and copying.

The important mental model is:

    name -> object

A variable is not a box that permanently owns a value. It is a name bound to
an object, and more than one name can point to the same object.
"""

from copy import deepcopy #Might Be a Global Import, but it's fine for a demo script


def demonstrate_references() -> dict[str, object]:
    """Return observable examples of references and equality.

    Returning the results instead of only printing them keeps this lesson easy
    to test and makes each claim explicit for someone learning the theory.
    """

    original = ["python"]
    alias = original

    # Assignment creates another name for the same list; it does not copy it.
    alias.append("backend")

    separately_created = ["python", "backend"]

    # ``==`` compares values. ``is`` compares object identity (the very same
    # object in memory). Use ``is`` mainly for identity checks such as None.
    equal_values = original == separately_created
    same_object = original is alias
    different_object = original is not separately_created

    nested = [["original"]]
    shallow_copy = nested.copy()
    deep_copy = deepcopy(nested)

    # A shallow copy creates a new outer list, but nested objects are shared.
    shallow_copy[0].append("changed through shallow copy")

    # A deep copy recursively copies nested objects, so it is independent.
    deep_copy[0].append("changed only in deep copy")

    number_before_rebinding = 10
    another_name = number_before_rebinding
    number_before_rebinding += 1

    # Integers are immutable. ``+=`` creates/binds a new integer object rather
    # than changing the integer that both names originally referred to.
    return {
        "alias_value": original,
        "equal_values": equal_values,
        "same_object": same_object,
        "different_object": different_object,
        "shallow_copy": shallow_copy,
        "deep_copy": deep_copy,
        "rebound_number": number_before_rebinding,
        "other_number_name": another_name,
    }


def demonstrate_truthiness_and_none() -> dict[str, object]:
    """Show common falsy values and the correct way to check for None."""

    falsy_values = [False, None, 0, 0.0, "", [], {}, set()]

    # ``bool(value)`` asks Python whether a value should be treated as true in
    # a condition. It does not convert every value to the string "True".
    return {
        "falsy_values": falsy_values,
        "all_are_falsy": all(not bool(value) for value in falsy_values),
        "none_is_none": None is None,
    }


if __name__ == "__main__":
    # This makes the file useful as a tiny lesson on its own:
    # ``python python_core/references.py``.
    from pprint import pprint

    pprint(demonstrate_references())
    pprint(demonstrate_truthiness_and_none())
