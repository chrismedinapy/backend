# Frontend HTTP contract tests

The backend test suite includes a browser-facing contract layer in
`data/tests/test_frontend_http_contract.py`.

These tests interact with the application only through HTTP requests and public API
responses. They intentionally avoid calling view methods directly so that route,
authentication, middleware, serializer, response-envelope, and multipart behavior are
validated together.

## Covered journeys

- login through `POST /api/v1/data/users/login/`;
- refresh-token rotation through `POST /api/v1/data/users/login/refresh/`;
- authenticated collection access with search, ordering, and pagination;
- standardized unauthorized and invalid-query errors;
- authenticated multipart CSV upload.

## Contract boundaries

The suite asserts stable response shapes rather than implementation details:

- authentication responses expose `access_token`, `refresh_token`, `token_type`,
  `expires_in`, and `user`;
- collection responses expose `count`, `next`, `previous`, and `results`;
- API failures use the top-level `error` envelope;
- multipart requests accept a JSON `customer` field and a `text/csv`
  `customer_csv` file.

Domain persistence is mocked only where the purpose of the test is the HTTP boundary.
Authentication, token rotation, request parsing, validation, middleware, and response
serialization execute through the real application stack.

## Execution

The contract layer runs inside the existing Django suite:

```bash
python manage.py test data.tests.test_frontend_http_contract --verbosity=2
```

No additional GitHub Actions workflow is required. The permanent `Django CI baseline`
workflow executes these tests and includes them in the global coverage gate.
