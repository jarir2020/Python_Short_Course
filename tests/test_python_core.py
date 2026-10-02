import unittest

from python_core.references import (
    demonstrate_references,
    demonstrate_truthiness_and_none,
)
from python_core.scope import demonstrate_legb


class PythonCoreLessonTests(unittest.TestCase):
    """Tests that turn the lesson's theoretical claims into checks."""

    def test_assignment_creates_an_alias_for_a_mutable_list(self) -> None:
        result = demonstrate_references()

        self.assertEqual(result["alias_value"], ["python", "backend"])
        self.assertTrue(result["same_object"])

    def test_equality_and_identity_are_different_questions(self) -> None:
        result = demonstrate_references()

        self.assertTrue(result["equal_values"])
        self.assertTrue(result["different_object"])

    def test_shallow_and_deep_copy_differ_for_nested_objects(self) -> None:
        result = demonstrate_references()

        self.assertEqual(
            result["shallow_copy"],
            [["original", "changed through shallow copy"]],
        )
        self.assertEqual(
            result["deep_copy"],
            [["original", "changed only in deep copy"]],
        )

    def test_immutable_integer_is_rebound_instead_of_changed(self) -> None:
        result = demonstrate_references()

        self.assertEqual(result["rebound_number"], 11)
        self.assertEqual(result["other_number_name"], 10)

    def test_common_falsy_values_and_none_identity(self) -> None:
        result = demonstrate_truthiness_and_none()

        self.assertTrue(result["all_are_falsy"])
        self.assertTrue(result["none_is_none"])

    def test_legb_lookup(self) -> None:
        self.assertEqual(
            demonstrate_legb(),
            {
                "local": "local",
                "enclosing": "enclosing",
                "global": "global",
                "builtin": 8,
            },
        )


if __name__ == "__main__":
    unittest.main()
