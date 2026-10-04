import unittest

from python_core.data_structures_and_oop import (
    demonstrate_data_structures,
    calculate_total,
    SimpleUser,
)


class DataStructuresAndOOPTests(unittest.TestCase):
    """Tests for Lesson 2 Python fundamentals."""

    def test_data_structures(self) -> None:
        result = demonstrate_data_structures()
        self.assertEqual(result["fruits"], ["apple", "banana", "cherry"])
        self.assertEqual(result["coordinates"], (10.0, 20.0))
        self.assertEqual(result["user_name"], "Alice")
        self.assertEqual(result["unique_numbers"], [1, 2, 3])

    def test_args_and_kwargs(self) -> None:
        # 10 + 20 + 30 + tax(5) + tip(2) = 67
        total = calculate_total(10, 20, 30, tax=5.0, tip=2.0)
        self.assertEqual(total, 67.0)

    def test_simple_user_oop(self) -> None:
        user = SimpleUser("jarir", "jarir@example.com")
        self.assertTrue(user.is_active)
        self.assertIn("Active", user.get_info())

        user.deactivate()
        self.assertFalse(user.is_active)
        self.assertIn("Inactive", user.get_info())


if __name__ == "__main__":
    unittest.main()
