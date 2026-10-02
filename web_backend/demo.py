"""Run the Phase 2 HTTP and SQL fundamentals lab."""

from pprint import pprint

from .http_lab import demo_server, describe_http_methods, request_json
from .sql_lab import create_library_database, run_sql_examples


def main() -> None:
    """Make local HTTP calls and run SQL examples without external services."""

    print("=== PHASE 2: WEB & BACKEND FUNDAMENTALS ===")

    print("\n--- HTTP methods ---")
    pprint(describe_http_methods())

    with demo_server() as base_url:
        print("\n--- HTTP request/response examples ---")
        pprint(request_json(f"{base_url}/health").__dict__)
        pprint(
            request_json(
                f"{base_url}/items",
                method="POST",
                payload={"name": "Python book"},
            ).__dict__
        )

    print("\n--- SQL examples ---")
    database = create_library_database()
    try:
        pprint(run_sql_examples(database))
    finally:
        database.close()


if __name__ == "__main__":
    main()
