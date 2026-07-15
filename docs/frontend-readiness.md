# Frontend readiness guide

This document is the integration entry point for frontend applications consuming DataCore. It consolidates the stable public contracts, local setup, production expectations, and validation commands already implemented by the backend.

## Readiness status

The backend is ready for frontend integration through the versioned API surface under `/api/v1/`.

The current baseline includes:

- versioned routes and health endpoints;
- explicit CORS and CSRF origin allowlists;
- OpenAPI schema, Swagger UI, and ReDoc;
- standardized JSON errors;
- access and refresh JWT contracts;
- pagination, search, filtering, and ordering;
- frontend-facing HTTP contract tests;
- a production Gunicorn runtime with health checks and request correlation.

## API entry points

Use only versioned routes for new integrations.

| Purpose | Path |
| --- | --- |
| API base | `/api/v1/` |
| Liveness | `/api/v1/health/live/` |
| Readiness | `/api/v1/health/ready/` |
| Compatibility health endpoint | `/api/v1/health/` |
| OpenAPI schema | `/api/schema/` |
| Swagger UI | `/api/docs/` |
| ReDoc | `/api/redoc/` |

The legacy `/data/` route may remain operational for compatibility, but frontend code must not depend on it.

## Authentication

### Login

```http
POST /api/v1/data/users/login/
Content-Type: application/json
```

```json
{
  "username": "frontend_user",
  "password": "replace-me"
}
```

Successful responses follow this contract:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "user_code": "...",
    "name": "...",
    "access_level": 1
  }
}
```

Send the access token on protected requests:

```http
Authorization: Bearer <access_token>
```

The scheme and spacing are strict. Cookie-based authentication must not be assumed.

### Refresh

```http
POST /api/v1/data/users/login/refresh/
Content-Type: application/json
```

```json
{
  "refresh_token": "..."
}
```

Refresh rotates the token pair. Replace both stored tokens with the values returned by the response.

## Error contract

API failures use one stable envelope:

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "Invalid parameter",
    "fields": {
      "email": ["Enter a valid email address."]
    }
  }
}
```

Frontend behavior must branch on `error.code`, not the human-readable message. The optional `error.fields` object contains field-level validation details.

Common status families include:

- `400` invalid input or query parameter;
- `401` missing, expired, or invalid authentication;
- `403` insufficient permission;
- `404` resource not found;
- `409` duplicate or conflicting state;
- `415` unsupported content type;
- `500` unexpected server error without internal exception leakage.

## Collection contract

Supported collection endpoints return:

```json
{
  "count": 125,
  "next": "https://api.example.test/api/v1/data/products/?page=2&page_size=20",
  "previous": null,
  "results": []
}
```

Supported query parameters depend on the endpoint and include:

- `page`;
- `page_size`, default `20`, maximum `100`;
- `search`;
- `ordering`, with descending order expressed as `-field`;
- endpoint-specific allowlisted filters such as `retail_store_city`.

Do not construct filters from arbitrary model fields. Unknown ordering fields are rejected through the standardized error contract.

## Multipart customer-input upload

The customer-input endpoint accepts multipart form data containing:

- `customer`, a JSON string;
- `customer_csv`, a `text/csv` file.

Route:

```text
/api/v1/data/customers/{customer_code}/retail-store/{retail_store_code}/products/
```

The frontend must let the browser or HTTP client generate the multipart boundary. Do not manually set a boundary in the `Content-Type` header.

## CORS and CSRF

Browser origins are deny-by-default. Every environment must explicitly configure comma-separated absolute origins.

```dotenv
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000
```

Production values must use the real HTTPS frontend origins. Do not include URL paths or trailing slashes.

## Local frontend configuration

A typical local frontend environment can use:

```dotenv
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

or the equivalent variable supported by the chosen frontend framework.

Recommended client responsibilities:

1. centralize the API base URL;
2. attach `Authorization: Bearer` through one request interceptor;
3. refresh once after an expired access token and retry the original request once;
4. replace both tokens after refresh;
5. normalize the `error` envelope in one place;
6. preserve pagination links instead of rebuilding them when practical;
7. generate or propagate an `X-Request-ID` for supportable requests.

## OpenAPI and TypeScript

Download the schema from `/api/schema/` or from the `openapi-contract` workflow artifact.

Example type generation:

```bash
npx openapi-typescript openapi.yaml -o src/api/generated/schema.d.ts
```

Generated files should be treated as build artifacts. Application-specific adapters and UI models should remain separate from generated schema types.

## Production runtime expectations

The production image runs:

```text
gunicorn core.wsgi:application --config python:gunicorn.conf
```

The application runs as a non-root user and exposes port `8000` by default. Deployment platforms should:

- terminate TLS at a trusted reverse proxy;
- configure `ALLOWED_HOSTS`, CORS, and CSRF origins explicitly;
- restrict `GUNICORN_FORWARDED_ALLOW_IPS` to trusted proxies;
- wait for the healthcheck before routing traffic;
- allow at least the configured graceful timeout during shutdown;
- collect stdout and stderr JSON logs;
- preserve `X-Request-ID` between proxy, backend, and frontend diagnostics.

Run the production security validation with production-like values:

```bash
DJANGO_SETTINGS_MODULE=core.settings_production python manage.py check --deploy
```

## Stable-contract checklist

Before starting frontend feature work, confirm:

- the environment exposes `/api/v1/health/` successfully;
- the frontend origin is present in `CORS_ALLOWED_ORIGINS`;
- login returns access and refresh tokens;
- protected requests use the Bearer header;
- refresh rotates and replaces both tokens;
- errors are handled through `error.code`;
- list screens support the pagination envelope;
- generated OpenAPI types match the deployed backend version;
- multipart uploads send JSON and CSV with the expected field names;
- production requests and logs expose a request ID.

## Detailed references

- `docs/api-versioning.md`
- `docs/frontend-settings.md`
- `docs/openapi.md`
- `docs/api-errors.md`
- `docs/authentication.md`
- `docs/api-listing.md`
- `docs/frontend-http-contract-tests.md`
- `docs/production-api-runtime.md`
