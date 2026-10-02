import unittest

from python_core.exceptions_and_context_managers import (
    safe_divide,
    validate_user_age,
    DatabaseValidationError,
    DummyDatabaseConnection,
)


class ExceptionAndContextTests(unittest.TestCase):
    """Unit tests for Lesson 3: Exception Handling and Context Managers."""

    def test_safe_divide_success(self) -> None:
        res = safe_divide(10, 2)
        self.assertEqual(res["result"], 5.0)
        self.assertIn("Success", res["status"])
        self.assertTrue(res["cleaned_up"])

    def test_safe_divide_zero_division(self) -> None:
        res = safe_divide(10, 0)
        self.assertIsNone(res["result"])
        self.assertIn("Error", res["status"])
        self.assertTrue(res["cleaned_up"])

    def test_custom_exception_raising(self) -> None:
        self.assertEqual(validate_user_age(25), "Adult")
        self.assertEqual(validate_user_age(15), "Minor")

        # Test that negative age raises custom DatabaseValidationError
        with self.assertRaises(DatabaseValidationError) as ctx:
            validate_user_age(-5)
        self.assertEqual(ctx.exception.error_code, 400)
        self.assertIn("negative", str(ctx.exception))

    def test_custom_context_manager(self) -> None:
        db = DummyDatabaseConnection("test_db")
        self.assertFalse(db.is_connected)

        with db as connection:
            self.assertTrue(connection.is_connected)

        # After exiting `with` block, __exit__ automatically disconnects
        self.assertFalse(db.is_connected)


if __name__ == "__main__":
    unittest.main()
