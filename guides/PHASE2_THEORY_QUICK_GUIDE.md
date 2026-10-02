# Phase 2: Web and Backend Fundamentals

## HTTP request and response

An HTTP request contains a method, URL, headers, and sometimes a body. The
server returns a status code, headers, and sometimes a body such as JSON.

```text
Client -- request --> Server
Client <-- response -- Server
```

Common methods:

* `GET` reads a resource and is safe and idempotent.
* `POST` creates or triggers an action and is usually neither safe nor
  idempotent.
* `PUT` replaces a resource and is intended to be idempotent.
* `PATCH` partially updates a resource; idempotency depends on the operation.
* `DELETE` removes a resource and is intended to be idempotent.

Useful status codes include `200 OK`, `201 Created`, `204 No Content`, `400 Bad
Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, and `500
Internal Server Error`.

## JSON and Content-Type

JSON is a text format for structured data. A request carrying JSON should send
`Content-Type: application/json`; the response should use the same header when
its body is JSON. Query parameters belong in the URL, while a JSON body carries
structured input for methods such as `POST` or `PUT`.

## SQL essentials

SQL works with tables and relationships. A parameterized query keeps values
separate from SQL instructions and helps prevent SQL injection:

```python
connection.execute(
    "SELECT title FROM books WHERE author_id = ?",
    (author_id,),
)
```

An `INNER JOIN` combines related rows through matching keys, for example
`books.author_id = authors.id`. The Phase 2 lab uses SQLite in memory, so it is
safe to run repeatedly without creating a database file.

Run the lab with:

```bash
python -m pip install -r requirements.txt
python -m web_backend.demo
python -m unittest discover -s tests -v
```
