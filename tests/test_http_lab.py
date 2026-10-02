import unittest

from web_backend.http_lab import demo_server, describe_http_methods, request_json


class HttpLabTests(unittest.TestCase):
    """Test HTTP behavior against the local deterministic server."""

    def test_method_semantics(self) -> None:
        methods = describe_http_methods()

        self.assertTrue(methods["GET"]["safe"])
        self.assertTrue(methods["PUT"]["idempotent"])
        self.assertFalse(methods["POST"]["idempotent"])

    def test_get_returns_json_and_status(self) -> None:
        with demo_server() as base_url:
            response = request_json(f"{base_url}/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, {"method": "GET", "path": "/health"})
        self.assertIn("application/json", response.headers["Content-Type"])

    def test_post_serializes_json_and_returns_created(self) -> None:
        with demo_server() as base_url:
            response = request_json(
                f"{base_url}/items",
                method="POST",
                payload={"name": "book"},
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.body["method"], "POST")
        self.assertEqual(response.body["payload"], {"name": "book"})

    def test_unsupported_teaching_method_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            request_json("http://127.0.0.1:1", method="TRACE")


if __name__ == "__main__":
    unittest.main()
