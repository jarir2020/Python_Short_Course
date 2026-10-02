"""A small executable example of Python's LEGB name lookup rule.

LEGB means Python looks for a name in this order:

    Local -> Enclosing -> Global -> Built-in
"""

GLOBAL_LABEL = "global"


def demonstrate_legb() -> dict[str, str | int]:
    """Return one value found at each level of the LEGB lookup rule."""

    enclosing_label = "enclosing"

    def read_names() -> dict[str, str | int]:
        local_label = "local"

        # ``enclosing_label`` is not local to this nested function, so Python
        # finds it in the surrounding function's scope (the E in LEGB).
        # ``GLOBAL_LABEL`` is found at module level (the G).
        # ``len`` is provided by Python itself (the B).
        return {
            "local": local_label,
            "enclosing": enclosing_label,
            "global": GLOBAL_LABEL,
            "builtin": len("built-in"),
        }

    return read_names()


if __name__ == "__main__":
    print(demonstrate_legb())
