# Celery CI integration

## Status

The Django CI workflow now validates end-to-end Celery task execution with the same application configuration used by the project.

## Architecture under test

The integration check exercises this complete path:

```text
core.settings_ci
→ core.settings
→ core.celery.app
→ RabbitMQ broker
→ Celery worker
→ CI healthcheck task
→ Redis result backend
→ result assertion
```

RabbitMQ remains the task broker. Redis database `1` is used only as an isolated CI result backend.

## CI task

The test task lives in `core/ci_tasks.py`:

```python
@app.task(name="core.ci_healthcheck")
def ci_healthcheck(value: str) -> dict[str, str]:
    return {
        "received": value,
        "status": "processed",
    }
```

The task is deterministic, has no database side effects and exists only to validate the asynchronous execution path.

## Worker configuration

GitHub Actions starts a real worker with:

```bash
celery -A core worker \
  --loglevel=INFO \
  --pool=solo \
  --concurrency=1 \
  --without-gossip \
  --without-mingle \
  --without-heartbeat \
  --include=core.ci_tasks
```

`pool=solo` and concurrency `1` keep the CI worker deterministic and avoid process-forking differences on hosted runners.

## Readiness validation

Before publishing the task, the workflow polls the worker using Celery control ping. The check fails if no worker responds within 20 seconds.

## End-to-end assertion

The workflow publishes the task with `.delay()` and retrieves the result through Redis:

```python
result = ci_healthcheck.delay("celery-is-ready")
output = result.get(timeout=20)
```

The expected result is:

```python
{
    "received": "celery-is-ready",
    "status": "processed",
}
```

This proves that task registration, serialization, RabbitMQ publication, worker consumption, task execution and result storage all work together.

## Failure diagnostics

The worker writes to `/tmp/celery-worker.log`. The workflow always prints the final 200 lines when the integration step exits, including startup and task-processing errors.

## Scope

This validation covers the Celery infrastructure path. It does not test production workload behavior, retries, scheduling, idempotency or application-specific tasks. Those behaviors should remain covered by focused application tests.
