"""Run the Phase 1 Python fundamentals lessons from the project root."""

from pprint import pprint

from .basics_and_control_flow import demonstrate_arithmetic_and_logic, evaluate_grade, demonstrate_loops_and_slicing
from .references import demonstrate_references, demonstrate_truthiness_and_none
from .scope import demonstrate_legb
from .data_structures_and_oop import demonstrate_data_structures, calculate_total, SimpleUser
from .exceptions_and_context_managers import safe_divide, validate_user_age, DatabaseValidationError, DummyDatabaseConnection
from .decorators_and_type_hints import process_payment, delete_database_record, Product
from .modules_and_env import explain_module_imports
from .iterables_and_generators import (
    count_up_to,
    demonstrate_comprehensions,
    demonstrate_dynamic_typing,
    demonstrate_functional_tools,
    demonstrate_iterator_protocol,
)


def main() -> None:
    """Print the lesson results in a readable form."""

    print("=== PHASE 1: PYTHON CORE ESSENTIALS FOR WEB DEVELOPERS ===")

    print("\n--- LESSON 0: Absolute Python Basics & Control Flow ---")
    print("1. Arithmetic & Logic (10, 3):")
    pprint(demonstrate_arithmetic_and_logic(10, 3))

    print("\n2. Grade Evaluation (if/elif/else):")
    print(evaluate_grade(85))

    print("\n3. Loops & List Slicing:")
    pprint(demonstrate_loops_and_slicing())

    print("\n--- LESSON 1: References, Mutability, and Scope ---")
    print("1. References, mutability, and copying:")
    pprint(demonstrate_references())

    print("\n2. Truthiness and None:")
    pprint(demonstrate_truthiness_and_none())

    print("\n3. LEGB scope lookup:")
    pprint(demonstrate_legb())

    print("\n--- LESSON 2: Data Structures, Functions & OOP ---")
    print("1. Data Structures:")
    pprint(demonstrate_data_structures())

    print("\n2. *args and **kwargs Function Calculation:")
    print(f"calculate_total(10, 20, 30, tax=5.0, tip=2.0) = {calculate_total(10, 20, 30, tax=5.0, tip=2.0)}")

    print("\n3. OOP SimpleUser Class:")
    user = SimpleUser("jarir", "jarir@example.com")
    print(f"Created: {user.get_info()}")
    user.deactivate()
    print(f"After deactivate(): {user.get_info()}")

    print("\n--- LESSON 3: Exception Handling & Context Managers ---")
    print("1. safe_divide(10, 0):", safe_divide(10, 0))
    try:
        validate_user_age(-5)
    except DatabaseValidationError as err:
        print(f"2. Caught custom exception: {err} (Code {err.error_code})")

    with DummyDatabaseConnection("production_db") as db:
        print(f"3. Context Manager active? {db.is_connected}")

    print("\n--- LESSON 4: Decorators, Type Hints & Dataclasses ---")
    print("1. Decorator Execution:")
    print(process_payment(250.0))

    print("2. Protected Admin Action Decorator:")
    print(delete_database_record("admin", 101))

    prod = Product(id=1, name="MacBook", price=1200.0)
    print(f"3. Dataclass item: {prod.name}, Discounted: ${prod.calculate_discounted_price(15):.2f}")

    print("\n--- LESSON 5: Modules, Packages & Virtual Environments ---")
    pprint(explain_module_imports())
    print("\n--- LESSON 6: Dynamic Typing, Comprehensions & Generators ---")
    pprint(demonstrate_dynamic_typing())
    pprint(demonstrate_comprehensions([1, 2, 2, 3, 4]))
    pprint(demonstrate_iterator_protocol())
    pprint(demonstrate_functional_tools([-2, -1, 0, 3]))
    print(f"count_up_to(3) = {list(count_up_to(3))}")

    print("\n✅ PHASE 1 COMPLETE!")


if __name__ == "__main__":
    main()
