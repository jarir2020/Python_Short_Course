"""Lesson 6: dynamic typing, comprehensions, iterators, and generators.

These concepts appear frequently in backend code. For example, a generator can
stream database rows or file lines without loading every item into memory at
once, while comprehensions are useful for shaping API data.
"""

from collections.abc import Iterable, Iterator, Sequence
from functools import reduce


def demonstrate_dynamic_typing() -> dict[str, object]:
    """Show that a name can be rebound to objects of different types.

    Python is dynamically typed: the *object* has a type, and a name can later
    refer to an object with a different type. The annotation below documents
    intent, but Python does not enforce it at runtime by itself.
    """

    value: object = "first value"
    initial_type = type(value).__name__

    value = 42
    return {
        "initial_type": initial_type,
        "final_type": type(value).__name__,
        "final_value": value,
    }


def demonstrate_comprehensions(numbers: Sequence[int]) -> dict[str, object]:
    """Build list, dictionary, and set comprehensions from one input."""

    # A list comprehension maps and/or filters values in one readable
    # expression: keep even numbers, then square them.
    even_squares = [number**2 for number in numbers if number % 2 == 0]

    # A dictionary comprehension creates key-value pairs from an iterable.
    parity_by_number = {
        number: "even" if number % 2 == 0 else "odd" for number in numbers
    }

    # A set comprehension automatically removes duplicate results.
    remainders_modulo_three = {number % 3 for number in numbers}

    return {
        "even_squares": even_squares,
        "parity_by_number": parity_by_number,
        "remainders_modulo_three": remainders_modulo_three,
    }


def demonstrate_iterator_protocol() -> dict[str, object]:
    """Show how ``iter`` and ``next`` consume an iterator one item at a time."""

    iterator = iter(["first", "second"])
    first_item = next(iterator)
    second_item = next(iterator)

    # Supplying a default prevents StopIteration when the iterator is empty.
    item_after_exhaustion = next(iterator, "no more items")

    return {
        "first_item": first_item,
        "second_item": second_item,
        "item_after_exhaustion": item_after_exhaustion,
    }


def count_up_to(limit: int) -> Iterator[int]:
    """Yield numbers lazily from 1 through ``limit``.

    ``yield`` turns this function into a generator function. Calling it does
    not run the loop immediately; execution pauses at each ``yield`` and
    resumes when the caller asks for the next item.
    """

    if limit < 0:
        raise ValueError("limit must be zero or greater")

    current = 1
    while current <= limit:
        yield current
        current += 1


def demonstrate_functional_tools(numbers: Iterable[int]) -> dict[str, object]:
    """Show ``map``, ``filter``, a lambda, and ``reduce``."""

    values = list(numbers)

    # ``lambda`` creates a small anonymous function. For complex behavior, a
    # named ``def`` is usually easier to read and debug.
    doubled = list(map(lambda number: number * 2, values))
    positive_values = list(filter(lambda number: number > 0, values))

    # reduce combines the sequence into one value. ``sum`` is clearer for
    # addition, but product is a compact example of the reduction operation.
    product = reduce(lambda left, right: left * right, values, 1)

    return {
        "doubled": doubled,
        "positive_values": positive_values,
        "product": product,
    }


if __name__ == "__main__":
    print(demonstrate_dynamic_typing())
    print(demonstrate_comprehensions([1, 2, 2, 3, 4]))
    print(list(count_up_to(3)))
