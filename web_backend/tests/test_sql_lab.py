import unittest

from web_backend.sql_lab import create_library_database, run_sql_examples


class SqlLabTests(unittest.TestCase):
    """Test relational queries against an in-memory SQLite database."""

    def test_sql_examples_cover_crud_and_join(self) -> None:
        database = create_library_database()
        try:
            result = run_sql_examples(database)
        finally:
            database.close()

        self.assertEqual(
            [book["title"] for book in result["books_over_25"]],
            ["SQL Basics", "Python Foundations", "Web APIs"],
        )
        self.assertEqual(result["unsafe_input_match_count"], 0)
        self.assertEqual(result["updated_price"], 40.0)
        self.assertEqual(result["joined_books"], [{
            "title": "HTTP Fundamentals",
            "author_name": "Ada Lovelace",
        }])
        self.assertEqual(result["deleted_rows"], 1)

    def test_foreign_key_constraint_is_enabled(self) -> None:
        database = create_library_database()
        try:
            with self.assertRaises(Exception):
                database.execute(
                    "INSERT INTO books (title, price, author_id) VALUES (?, ?, ?)",
                    ("Invalid", 1.0, 999),
                )
        finally:
            database.close()


if __name__ == "__main__":
    unittest.main()
