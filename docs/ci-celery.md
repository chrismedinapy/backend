# Celery CI integration

## Status

The Django CI workflow validates the complete asynchronous Celery infrastructure path with real RabbitMQ and Redis services. The final infrastructure implementation was validated successfully by workflow run #112.

This is an end-to-end test of the Celery subsystem. Production retry, idempotency, duplicate-delivery, and concurrency behavior is covered separately by [`docs/ci-celery-reliability.md`](ci-celery-reliability.md).

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

## CI tasks

The deterministic integration tasks live in `core/ci_tasks.py`.

The healthcheck task records proof that a separate worker consumed a message:

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

The retry probe intentionally fails its first execution and succeeds on the second. It is used by the Django reliability suite to confirm the exact retry attempt count and recovery marker.

These tasks have no PostgreSQL or MongoDB side effects. They write short-lived markers to Redis database `1`, which is isolated from the normal Redis cache validation.

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

`pool=solo` and concurrency `1` keep the infrastructure check deterministic on hosted runners. The explicit application path and task include remove CLI and autodiscovery ambiguity.

Production concurrency is not inferred from this command. The application reliability tests validate concurrent duplicate persistence separately, while deployment-specific worker topology remains outside the repository.

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

## What the infrastructure test proves

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

## Complementary reliability coverage

Workflow run #150 additionally validates:

- a deterministic task retry and recovery;
- bounded transient retry configuration on the production task;
- late acknowledgement and worker-loss rejection;
- deterministic GridFS identifiers;
- duplicate-delivery idempotency;
- concurrent duplicate persistence;
- explicit absence of a Celery Beat schedule.

Those guarantees and their limits are documented in [`docs/ci-celery-reliability.md`](ci-celery-reliability.md).

## What remains outside the infrastructure test

The infrastructure healthcheck by itself does not cover:

- HTTP endpoints or authentication;
- production business-task argument contracts;
- PostgreSQL or MongoDB side effects inside a Celery task;
- dead-letter behavior or poison-message routing;
- operating-system worker termination and RabbitMQ redelivery after a crash;
- deployment-specific pool type, process count, autoscaling, CPU limits, or queue routing;
- production containers, secrets, networking, or deployment configuration.

The application-specific business-flow and reliability suites complement these boundaries without claiming to certify deployment topology.

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

Workflow run #150 completed successfully with the additional retry, idempotency, concurrency, and scheduled-task-scope tests.
