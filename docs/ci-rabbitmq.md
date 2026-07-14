# RabbitMQ CI integration

## Status

The Django CI workflow starts a RabbitMQ broker and validates a complete message round trip before migrations and tests run.

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

The project already depends on `kombu` through Celery. CI uses that dependency to:

1. connect to RabbitMQ with the CI credentials;
2. create the temporary queue `ci-rabbitmq-integration`;
3. publish a JSON message;
4. consume the same message;
5. compare the received payload with the original payload;
6. acknowledge the message;
7. delete the temporary queue.

The validation fails if the connection, publication, consumption, serialization or acknowledgement fails.

## CI credentials

The isolated CI broker uses:

```text
user: core
password: core
virtual host: /
```

These values are deterministic test credentials and must not be reused in production.

## Scope

This check validates the broker and the Python AMQP client stack. It does not yet start a Celery worker or execute an application task. Celery worker and task execution are the next roadmap stage.
