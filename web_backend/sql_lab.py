"""A SQLite lab for CRUD, parameterized queries, and JOINs."""

from __future__ import annotations

import sqlite3
from typing import Any


def create_library_database() -> sqlite3.Connection:
    """Create a small relational database in memory.

    SQLite is a real SQL database engine, but ``:memory:`` means the lesson
    leaves no database file behind. Foreign-key enforcement is enabled
    explicitly because SQLite does not enable it by default for every setup.
    """

    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    with connection:
        connection.executescript(
            """
            CREATE TABLE authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES authors (id)
            );
            """
        )
        connection.executemany(
            "INSERT INTO authors (id, name) VALUES (?, ?)",
            [(1, "Ada Lovelace"), (2, "Grace Hopper")],
        )
        connection.executemany(
            "INSERT INTO books (title, price, author_id) VALUES (?, ?, ?)",
            [
                ("Python Foundations", 30.0, 1),
                ("Web APIs", 40.0, 2),
                ("SQL Basics", 25.0, 1),
            ],
        )

    return connection


def _rows(connection: sqlite3.Connection, query: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Execute a query and convert SQLite rows into ordinary dictionaries."""

    return [dict(row) for row in connection.execute(query, parameters).fetchall()]


def run_sql_examples(connection: sqlite3.Connection) -> dict[str, object]:
    """Demonstrate SELECT, INSERT, UPDATE, DELETE, filtering, and a JOIN."""

    books_over_25 = _rows(
        connection,
        "SELECT title, price FROM books WHERE price >= ? ORDER BY price",
        (25.0,),
    )

    # Parameters keep data separate from SQL instructions. Never build a query
    # by concatenating user input into the SQL string.
    safe_search_term = "%Python%' OR 1=1 --"
    safe_search = _rows(
        connection,
        "SELECT title FROM books WHERE title LIKE ?",
        (safe_search_term,),
    )

    with connection:
        insert_cursor = connection.execute(
            "INSERT INTO books (title, price, author_id) VALUES (?, ?, ?)",
            ("HTTP Fundamentals", 35.0, 1),
        )
        inserted_book_id = insert_cursor.lastrowid

        connection.execute(
            "UPDATE books SET price = price + ? WHERE id = ?",
            (5.0, inserted_book_id),
        )
        updated_price = connection.execute(
            "SELECT price FROM books WHERE id = ?", (inserted_book_id,)
        ).fetchone()["price"]

        joined_books = _rows(
            connection,
            """
            SELECT books.title, authors.name AS author_name
            FROM books
            JOIN authors ON authors.id = books.author_id
            WHERE books.id = ?
            """,
            (inserted_book_id,),
        )

        delete_cursor = connection.execute(
            "DELETE FROM books WHERE id = ?", (inserted_book_id,)
        )

    return {
        "books_over_25": books_over_25,
        "unsafe_input_match_count": len(safe_search),
        "inserted_book_id": inserted_book_id,
        "updated_price": updated_price,
        "joined_books": joined_books,
        "deleted_rows": delete_cursor.rowcount,
    }


if __name__ == "__main__":
    database = create_library_database()
    try:
        print(run_sql_examples(database))
    finally:
        database.close()
