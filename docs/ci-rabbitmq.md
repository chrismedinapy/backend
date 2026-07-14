# RabbitMQ CI integration

## Status

The Django CI workflow starts a RabbitMQ broker and verifies that the project's real Celery configuration can authenticate and establish an AMQP connection before migrations and tests run.

## Service configuration

GitHub Actions starts the following service:

```yaml
rabbitmq:
  image: rabbitmq:4-management-alpine
  env:
    RABBITMQ_DEFAULT_USER: core
    RABBITMQ_DEFAULT_PASS: core
    RABBITMQ_DEFAULT_VHOST: /
  ports:
    - 5672:5672
    - 15672:15672
```

The AMQP port is exposed on `5672`. Port `15672` exposes the management interface for diagnostics when needed.

## Health check

The workflow waits for RabbitMQ to become ready with:

```bash
rabbitmq-diagnostics -q ping
```

This prevents the application-level validation from starting while the broker is still initializing.

## Integration validation

CI imports `core.celery.app`, loads `CELERY_BROKER_URL` through `core.settings_ci` and `core.settings`, and opens a write connection with:

```python
with app.connection_for_write(connect_timeout=5) as connection:
    connection.ensure_connection(max_retries=3)
```

The validation proves that:

1. the project's Celery configuration loads correctly;
2. the generated broker URL is present;
3. the installed Celery, Kombu and AMQP packages can use the configured transport;
4. RabbitMQ accepts the configured user, password and virtual host;
5. a real TCP and AMQP connection can be established.

## CI credentials

The isolated CI broker uses:

```text
user: core
password: core
virtual host: /
```

These values are deterministic test credentials and must not be reused in production.

## Scope

This check validates RabbitMQ broker connectivity through the real Celery application configuration. It intentionally does not publish an application task or start a worker. Publishing, worker consumption and task-result validation belong to the next Celery integration stage, where they can be tested end to end without duplicating Celery's internal messaging implementation.
