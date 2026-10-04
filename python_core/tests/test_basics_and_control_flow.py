import unittest

from python_core.basics_and_control_flow import (
    demonstrate_arithmetic_and_logic,
    evaluate_grade,
    demonstrate_loops_and_slicing,
)


class BasicsAndControlFlowTests(unittest.TestCase):
    """Unit tests for Lesson 0: Absolute Python Basics & Control Flow."""

    def test_arithmetic_and_logic(self) -> None:
        res = demonstrate_arithmetic_and_logic(10, 3)
        self.assertEqual(res["addition"], 13)
        self.assertEqual(res["integer_division"], 3)
        self.assertEqual(res["modulo_remainder"], 1)
        self.assertEqual(res["exponent_power"], 1000)
        self.assertFalse(res["is_equal"])
        self.assertTrue(res["logical_and"])

    def test_evaluate_grade_control_flow(self) -> None:
        self.assertIn("Grade: A (Passed)", evaluate_grade(95))
        self.assertIn("Grade: B (Passed)", evaluate_grade(82))
        self.assertIn("Grade: F (Failed)", evaluate_grade(50))

    def test_loops_and_slicing(self) -> None:
        res = demonstrate_loops_and_slicing()
        self.assertEqual(res["first_item"], 10)
        self.assertEqual(res["last_item"], 50)
        self.assertEqual(res["middle_slice"], [20, 30, 40])
        self.assertEqual(res["range_sum"], 15)  # 1+2+3+4+5
        self.assertEqual(res["countdown"], [3, 2, 1])


if __name__ == "__main__":
    unittest.main()
