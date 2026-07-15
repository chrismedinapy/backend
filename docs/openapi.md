# OpenAPI and interactive API documentation

DataCore publishes a machine-readable OpenAPI contract and two interactive documentation interfaces.

## Endpoints

| Endpoint | Purpose |
| --- | --- |
| `/api/schema/` | Raw OpenAPI schema |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |

Only the versioned `/api/v1/` surface is included in the generated contract. The deprecated `/data/` compatibility route remains operational but is intentionally excluded so new clients do not depend on it.

## Authentication

Authenticated operations use the OpenAPI security scheme `bearerAuth`:

```http
Authorization: Bearer <access-token>
```

The scheme is declared as HTTP Bearer with JWT format. Swagger UI therefore exposes an **Authorize** action for supplying an access token.

## Generate and validate locally

Use the CI settings for a deterministic schema build:

```bash
DJANGO_SETTINGS_MODULE=core.settings_ci \
python manage.py spectacular --validate --file openapi.yaml
```

The command fails when the generated document contains OpenAPI validation errors.

## Generate TypeScript types

The CI workflow publishes `openapi.yaml` as the `openapi-contract` artifact. A frontend repository can consume that artifact with a generator such as `openapi-typescript`:

```bash
npx openapi-typescript openapi.yaml -o src/api/generated/schema.d.ts
```

Generated files should be treated as build artifacts. Do not edit them manually; update the backend schema and regenerate them instead.

## CI contract

The `OpenAPI contract` workflow:

1. installs the pinned backend dependencies;
2. generates the schema with validation enabled;
3. asserts that every documented route starts with `/api/v1/`;
4. rejects accidental publication of deprecated `/data/` routes;
5. validates the Bearer JWT security definition;
6. uploads `openapi.yaml` for frontend use.

When `drf-spectacular` is upgraded, review the generated schema diff before merging because schema-generator updates can affect generated client code.
