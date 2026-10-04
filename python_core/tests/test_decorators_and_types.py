import unittest

from python_core.decorators_and_type_hints import (
    process_payment,
    delete_database_record,
    Product,
)


class DecoratorAndTypeHintTests(unittest.TestCase):
    """Unit tests for Lesson 4: Decorators, Type Hints, and Dataclasses."""

    def test_log_execution_decorator(self) -> None:
        result = process_payment(99.99)
        self.assertEqual(result, "Payment of $99.99 processed.")
        # Ensure functools.wraps preserved the function name
        self.assertEqual(process_payment.__name__, "process_payment")

    def test_require_role_decorator_success(self) -> None:
        result = delete_database_record("admin", 42)
        self.assertEqual(result, "Record 42 deleted by admin.")

    def test_require_role_decorator_permission_denied(self) -> None:
        with self.assertRaises(PermissionError):
            delete_database_record("user", 42)

    def test_product_dataclass(self) -> None:
        item = Product(id=1, name="Laptop", price=1000.0)
        self.assertEqual(item.name, "Laptop")
        self.assertIsNone(item.description)
        self.assertEqual(item.calculate_discounted_price(10), 900.0)


if __name__ == "__main__":
    unittest.main()
