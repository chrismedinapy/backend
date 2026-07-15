# API versioning and compatibility

The stable frontend-facing API is exposed below the `/api/v1/` prefix.

## Current routes

| Route | Purpose | Status |
| --- | --- | --- |
| `GET /health/` | Unversioned service health check for infrastructure | Supported |
| `GET /api/v1/health/` | Versioned API health check | Supported |
| `/api/v1/data/` | Versioned DataCore API routes | Preferred |
| `/data/` | Original DataCore API routes | Deprecated compatibility alias |

Both health endpoints return the following stable response when the Django
process is available:

```json
{
  "status": "ok",
  "service": "datacore-api"
}
```

The health check confirms that Django can serve an HTTP request. It does not
currently verify PostgreSQL, Redis, MongoDB, RabbitMQ, or Celery availability.
Dependency readiness checks should be introduced separately if the deployment
platform requires them.

## Deprecation policy for `/data/`

Existing consumers may continue using `/data/` temporarily. New integrations
must use `/api/v1/data/`.

Removal of `/data/` requires all of the following:

1. known consumers have migrated to `/api/v1/data/`;
2. the removal is announced in release notes;
3. contract tests no longer depend on the compatibility route;
4. a separate breaking-change pull request removes the alias.
