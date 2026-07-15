# Celery CI integration

## Status

The Django CI workflow validates the complete asynchronous Celery infrastructure path with real RabbitMQ and Redis services. The final implementation was validated successfully by workflow run #112.

This is an end-to-end test of the Celery subsystem. It is not an end-to-end test of every application business flow.

## Architecture under test

The integration check exercises this path:

```text
core.settings_ci
→ core.settings
→ core.celery.app
→ RabbitMQ broker
→ separate Celery worker process
→ core.ci_healthcheck
→ Redis database 1 execution marker
→ marker assertion
```

The producer and worker run as separate processes. The task is published through RabbitMQ with `.delay()` and is not executed eagerly or called directly.

## Isolated CI settings

GitHub Actions sets:

```yaml
env:
  DJANGO_SETTINGS_MODULE: core.settings_ci
```

`core/settings_ci.py` imports the normal project settings and overrides only values required by automated checks. The Celery-specific CI configuration includes:

```python
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXPIRES = 300
CELERY_WORKER_ENABLE_REMOTE_CONTROL = False
CELERY_IMPORTS = ("core.ci_tasks",)
```

`CELERY_IMPORTS` is required because `core` is the project package rather than a Django application, so normal Celery task autodiscovery does not scan it.

## RabbitMQ 4 compatibility

Celery remote control normally creates a `pidbox` queue for commands such as `inspect`, `ping`, `broadcast` and `revoke`.

RabbitMQ 4 rejects the deprecated transient non-exclusive queue type used by that optional subsystem when the `transient_nonexcl_queues` compatibility feature is disabled. The CI worker does not need remote-control commands, so they are disabled only in `settings_ci.py`:

```python
CELERY_WORKER_ENABLE_REMOTE_CONTROL = False
```

This does not disable normal task publication, queue consumption or task execution.

## CI task

The deterministic integration task lives in `core/ci_tasks.py`:

```python
@app.task(name="core.ci_healthcheck", ignore_result=True)
def ci_healthcheck(value: str, marker_key: str) -> None:
    client = Redis(host="localhost", port=6379, db=1, decode_responses=True)
    payload = {
        "received": value,
        "status": "processed",
    }
    client.set(marker_key, json.dumps(payload, sort_keys=True), ex=60)
    client.close()
```

The task has no PostgreSQL or MongoDB side effects. It writes a short-lived marker to Redis database `1`, which is isolated from the normal Redis cache validation.

## Worker configuration

GitHub Actions starts a real worker process with:

```bash
celery -A core.celery:app worker \
  --pool=solo \
  --concurrency=1 \
  --loglevel=WARNING \
  --without-gossip \
  --without-mingle \
  --without-heartbeat \
  --include=core.ci_tasks
```

`pool=solo` and concurrency `1` keep execution deterministic on hosted runners. The explicit application path and task include remove CLI and autodiscovery ambiguity.

## End-to-end assertion

The workflow creates a unique Redis marker key and publishes the task through RabbitMQ:

```python
marker_key = f"ci:celery:{uuid.uuid4()}"
result = ci_healthcheck.delay("celery-is-ready", marker_key)
```

It then polls Redis database `1` for at most 20 seconds. The expected marker is:

```python
{
    "received": "celery-is-ready",
    "status": "processed",
}
```

The marker key is deleted after validation, whether the test succeeds or fails.

The test intentionally does not use `AsyncResult.get()`. The marker provides independent evidence that the separate worker consumed and executed the task while keeping the check focused on the broker and worker path.

## What the test proves

A successful check confirms that the tested versions and configuration can perform all of the following together:

- load `core.settings_ci` and the real Celery application;
- build and authenticate the RabbitMQ broker connection;
- register the CI task in the worker;
- serialize and publish a task message;
- create and consume the Celery task queue;
- start a separate worker process;
- receive and execute the task;
- connect from the worker to Redis;
- persist and validate the expected execution marker.

This gives strong regression protection for the Celery, RabbitMQ and Redis integration contract represented by this test.

## What the test does not prove

A green check does not guarantee that every production workflow is correct. This test does not cover:

- HTTP endpoints or authentication;
- production business tasks and their argument contracts;
- PostgreSQL or MongoDB side effects inside a Celery task;
- retries, acknowledgements after failure or dead-letter behavior;
- idempotency and duplicate delivery handling;
- Celery Beat or scheduled tasks;
- multiple workers or production concurrency pools;
- production containers, secrets, networking or deployment configuration.

Application-specific asynchronous workflows should have additional integration tests that publish a real business task and assert its persisted business effect.

## Failure diagnostics

The worker writes to:

```text
/tmp/celery-worker.log
```

The workflow prints the final 120 lines when the integration step exits.

The separate `Upload Celery worker diagnostics` step uses:

```yaml
if: failure()
```

Therefore it is expected to appear as `skipped` when the job is successful. When an earlier step fails, the full worker log is uploaded as the `celery-worker-diagnostics` artifact and retained for three days.

## Validation result

Workflow run #112 completed successfully, including:

- Redis cache integration;
- MongoDB CRUD integration;
- RabbitMQ connectivity through the Celery configuration;
- end-to-end Celery task publication and worker execution;
- migration checks and application;
- the Django test suite;
- the 70% coverage gate and coverage artifact.
