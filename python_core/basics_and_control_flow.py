"""Lesson 0: Absolute Python Basics (Operators, Control Flow, Loops, and Slicing).

===============================================================================
THEORY CONCEPT: PROGRAMMING BASICS IN PYTHON
===============================================================================
Every Python program relies on fundamental building blocks:
1. Arithmetic Operators: `+` (add), `-` (subtract), `*` (multiply), `/` (float divide),
   `//` (floor/integer divide), `%` (modulo/remainder), `**` (exponent/power).
2. Comparison & Logical Operators: `==`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, `not`.
3. Control Flow (`if / elif / else`): Executing code conditionally based on true/false statements.
4. Loops (`for`, `while`): Repeating actions over sequences or while a condition remains True.
5. Indexing & Slicing: Accessing single elements or sub-ranges in arrays/lists.
"""

def demonstrate_arithmetic_and_logic(a: int, b: int) -> dict:
    """Show standard arithmetic and comparison operations."""
    return {
        "addition": a + b,
        "subtraction": a - b,
        "multiplication": a * b,
        "float_division": a / b,         # 10 / 3 = 3.3333...
        "integer_division": a // b,      # 10 // 3 = 3
        "modulo_remainder": a % b,       # 10 % 3 = 1
        "exponent_power": a ** b,        # 10 ** 3 = 1000
        "is_equal": a == b,
        "logical_and": (a > 0) and (b > 0)
    }


def evaluate_grade(score: int) -> str:
    """Demonstrate if / elif / else control flow and ternary operator."""

    # Standard control flow
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"

    # Ternary operator syntax: <val_if_true> if <condition> else <val_if_false>
    status = "Passed" if score >= 70 else "Failed"

    return f"Grade: {grade} ({status})"


def demonstrate_loops_and_slicing() -> dict:
    """Show for loops, while loops, range(), list indexing, and array slicing."""

    # 1. Array / List Indexing & Slicing
    numbers = [10, 20, 30, 40, 50]
    first_item = numbers[0]              # 10
    last_item = numbers[-1]              # 50 (negative index counts from end)
    middle_slice = numbers[1:4]          # [20, 30, 40] (from index 1 up to 4, excluding 4)

    # 2. For Loop with range(start, stop)
    loop_sum = 0
    for i in range(1, 6):                # 1, 2, 3, 4, 5
        loop_sum += i

    # 3. While Loop
    counter = 3
    countdown = []
    while counter > 0:
        countdown.append(counter)
        counter -= 1

    return {
        "first_item": first_item,
        "last_item": last_item,
        "middle_slice": middle_slice,
        "range_sum": loop_sum,
        "countdown": countdown
    }
