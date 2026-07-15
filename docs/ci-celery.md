# Celery CI integration

## Status

The Django CI workflow validates the complete asynchronous Celery infrastructure path with real RabbitMQ and Redis services. The deterministic infrastructure implementation was validated successfully by workflow run #112.

The workflow also validates one production asynchronous customer-input flow across the API, PostgreSQL/PostGIS, file storage, RabbitMQ, a separate Celery worker and MongoDB GridFS. That business-flow check first passed in workflow run #137.

These checks serve different purposes:

- the deterministic healthcheck isolates the Celery infrastructure contract;
- the customer-input flow validates one real production endpoint, task and persisted business effect.

## Infrastructure architecture under test

The deterministic integration check exercises this path:

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

Production tasks in the `data` Django application are registered through `data/tasks.py`, which re-exports the existing implementation from `data/task/create_customer_input_dataset.py`. A normal worker startup can therefore discover the production task without CI-only include arguments.

## RabbitMQ 4 compatibility

Celery remote control normally creates a `pidbox` queue for commands such as `inspect`, `ping`, `broadcast` and `revoke`.

RabbitMQ 4 rejects the deprecated transient non-exclusive queue type used by that optional subsystem when the `transient_nonexcl_queues` compatibility feature is disabled. The CI worker does not need remote-control commands, so they are disabled only in `settings_ci.py`:

```python
CELERY_WORKER_ENABLE_REMOTE_CONTROL = False
```

This does not disable normal task publication, queue consumption or task execution.

## Deterministic CI task

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

## Infrastructure worker configuration

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

`pool=solo` and concurrency `1` keep execution deterministic on hosted runners. The explicit application path and task include remove CLI and project-package discovery ambiguity.

## Infrastructure end-to-end assertion

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

## Application-specific asynchronous flow

After database migrations, the workflow starts another separate worker without an explicit task include and runs:

```bash
python scripts/ci/validate_async_customer_input_flow.py
```

The script calls the real authenticated multipart CSV endpoint. The endpoint creates a `CustomerInput`, stores the CSV, publishes the production `create_collection` task, and waits for the worker to persist the parsed dataset in MongoDB GridFS and write the resulting identifier back to PostgreSQL.

The detailed endpoint contract, fixture setup, persistence assertions, cleanup and diagnostics are documented in [`docs/ci-async-business-flow.md`](ci-async-business-flow.md).

## What the infrastructure test proves

A successful deterministic check confirms that the tested versions and configuration can perform all of the following together:

- load `core.settings_ci` and the real Celery application;
- build and authenticate the RabbitMQ broker connection;
- register the CI task in the worker;
- serialize and publish a task message;
- create and consume the Celery task queue;
- start a separate worker process;
- receive and execute the task;
- connect from the worker to Redis;
- persist and validate the expected execution marker.

This gives focused regression protection for the Celery, RabbitMQ and Redis integration contract represented by this test.

## What the combined checks prove

Together, the infrastructure and business-flow stages also confirm one real production contract involving:

- HTTP routing, authentication and multipart request handling;
- PostgreSQL metadata persistence;
- application file storage;
- production-task autodiscovery;
- RabbitMQ publication and delivery;
- separate worker execution;
- MongoDB GridFS persistence;
- cross-database state propagation back to PostgreSQL.

## Scope boundaries

A green workflow does not guarantee that every asynchronous production workflow is correct. The current checks do not cover:

- every production task and argument contract;
- retries, acknowledgements after failure or dead-letter behavior;
- idempotency and duplicate delivery handling;
- Celery Beat or scheduled tasks;
- multiple workers or production concurrency pools;
- large-file performance and resource limits;
- production secrets, networking or deployment configuration.

Additional business flows should be added when they represent materially different task contracts or failure modes.

## Failure diagnostics

The deterministic worker writes to:

```text
/tmp/celery-worker.log
```

The workflow prints the final 120 lines when the integration step exits.

The separate `Upload Celery worker diagnostics` step uses:

```yaml
if: failure()
```

Therefore it is expected to appear as `skipped` when the job is successful. When an earlier step fails, the full worker log is uploaded as the `celery-worker-diagnostics` artifact and retained for three days.

The business-flow worker and script write to:

```text
/tmp/celery-business-worker.log
/tmp/async-business-flow.log
```

When the business-flow stage fails, both files are uploaded as the `async-business-flow-diagnostics` artifact. That upload step is also expected to be `skipped` on success.

## Validation results

Workflow run #112 completed successfully with the deterministic Celery infrastructure check.

Workflow run #137 completed successfully with:

- Redis cache integration;
- MongoDB CRUD integration;
- RabbitMQ connectivity through the Celery configuration;
- deterministic Celery task publication and worker execution;
- authenticated asynchronous customer-input business-flow validation;
- migration checks and application;
- the Django test suite;
- the 70% coverage gate and coverage artifact.