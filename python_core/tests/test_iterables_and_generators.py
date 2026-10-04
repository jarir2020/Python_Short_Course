import unittest

from python_core.iterables_and_generators import (
    count_up_to,
    demonstrate_comprehensions,
    demonstrate_dynamic_typing,
    demonstrate_functional_tools,
    demonstrate_iterator_protocol,
)


class IterablesAndGeneratorTests(unittest.TestCase):
    """Tests that connect iterable theory to observable behavior."""

    def test_dynamic_typing_rebinds_a_name(self) -> None:
        self.assertEqual(
            demonstrate_dynamic_typing(),
            {
                "initial_type": "str",
                "final_type": "int",
                "final_value": 42,
            },
        )

    def test_comprehensions_build_different_data_structures(self) -> None:
        result = demonstrate_comprehensions([1, 2, 2, 3, 4])

        self.assertEqual(result["even_squares"], [4, 4, 16])
        self.assertEqual(result["parity_by_number"][3], "odd")
        self.assertEqual(result["remainders_modulo_three"], {0, 1, 2})

    def test_iterator_protocol_consumes_items(self) -> None:
        self.assertEqual(
            demonstrate_iterator_protocol(),
            {
                "first_item": "first",
                "second_item": "second",
                "item_after_exhaustion": "no more items",
            },
        )

    def test_generator_yields_values_lazily(self) -> None:
        generator = count_up_to(3)

        self.assertEqual(next(generator), 1)
        self.assertEqual(list(generator), [2, 3])

    def test_generator_rejects_negative_limits(self) -> None:
        with self.assertRaises(ValueError):
            list(count_up_to(-1))

    def test_functional_tools(self) -> None:
        self.assertEqual(
            demonstrate_functional_tools([-2, -1, 0, 3]),
            {
                "doubled": [-4, -2, 0, 6],
                "positive_values": [3],
                "product": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
