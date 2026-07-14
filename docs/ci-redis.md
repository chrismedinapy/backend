# Redis CI integration

## Status

The Django CI pipeline now validates Redis connectivity and cache operations using a real Redis 7.4 service container. The integration was validated successfully by workflow run #71.

## What changed

- GitHub Actions starts `redis:7.4-alpine` alongside PostgreSQL/PostGIS.
- Redis availability is checked with `redis-cli ping` before application validation begins.
- The pipeline performs a real cache round trip through `django.core.cache`.
- Redis configuration supports deployments with or without a password.
- CI uses an isolated passwordless Redis instance, while production may continue using `REDIS_PASSWORD`.

## Service configuration

```yaml
redis:
  image: redis:7.4-alpine
  ports:
    - 6379:6379
  options: >-
    --health-cmd "redis-cli ping"
    --health-interval 10s
    --health-timeout 5s
    --health-retries 10
```

## Application validation

The pipeline validates Redis through Django rather than only checking the TCP port:

```python
from django.core.cache import cache

cache.set("ci:redis-health", "ok", timeout=30)
assert cache.get("ci:redis-health") == "ok"
cache.delete("ci:redis-health")
assert cache.get("ci:redis-health") is None
```

This proves that the configured Django cache backend can connect, write, read and delete values.

## Environment behavior

The Redis URL is built according to whether `REDIS_PASSWORD` is present:

```text
redis://host:port
redis://:password@host:port
```

CI defaults to:

```text
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

No production credential is stored in the workflow or repository.

## Pipeline order

Redis validation runs after dependency installation and the Django system check, and before migrations and the full test suite. A Redis integration failure therefore stops the pipeline early.

## Scope

This integration validates Django cache operations only. It does not yet validate:

- Redis as a Celery broker or result backend;
- distributed locking or queues;
- Redis persistence or failover;
- production TLS or authentication policies.

Those areas can be covered in later integration stages.
