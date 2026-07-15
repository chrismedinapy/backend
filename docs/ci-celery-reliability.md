# Celery retries, idempotency, and concurrency validation

## Status

The CI baseline validates the reliability contract used by the production CSV-ingestion Celery task.

The first successful validation completed in Django CI workflow run #150. The production Docker image also passed its dedicated workflow for the same implementation head in run #22.

## Production task policy

`data.task.create_customer_input_dataset.create_collection` uses:

```text
bind=True
acks_late=True
reject_on_worker_lost=True
max_retries=3
```

The task retries only when the exception chain contains a transient dependency error from MongoDB or PostgreSQL. The retry countdown uses bounded exponential backoff:

```text
1 second
2 seconds
4 seconds
```

The maximum countdown is capped at 30 seconds.

Non-transient failures, including invalid CSV data and missing application records, are not retried automatically.

## Retry validation

The CI-only task `core.ci_retry_probe` provides deterministic evidence that Celery retry behavior works:

```text
first execution
→ intentional failure
→ Celery retry
→ second execution
→ Redis marker with attempts=2 and status=recovered
```

The Django reliability test executes the task eagerly and verifies the exact attempt count and final marker. RabbitMQ publication and separate-worker execution remain covered by the existing Celery end-to-end healthcheck.

## Idempotent GridFS persistence

The production persistence layer derives a stable GridFS `ObjectId` from `customer_input_code`.

```text
customer_input_code
→ SHA-256 digest
→ first 12 bytes
→ deterministic ObjectId
```

Repeated delivery of the same message therefore targets the same GridFS object rather than creating a new object on every execution.

If another worker completes the same write first, duplicate-key and GridFS file-exists errors are treated as successful convergence. PostgreSQL is then updated with the same stable `gridfs_code`.

## Duplicate-delivery validation

The real asynchronous business-flow script republishes the production task four times after the initial API-driven execution and verifies:

- every delivery returns the same GridFS identifier;
- PostgreSQL retains the same `gridfs_code`;
- exactly one matching record exists in `fs.files`;
- exactly one GridFS file is associated with the `CustomerInput` metadata.

The Django reliability suite also performs four simultaneous persistence calls through a thread pool against the real PostgreSQL and MongoDB CI services. This exercises the shared persistence boundary under concurrent duplicate delivery.

## Scheduled-task scope

The repository currently has:

- no `CELERY_BEAT_SCHEDULE` or `beat_schedule` entries;
- no periodic-task decorators;
- no `django-celery-beat` dependency.

The CI suite asserts that the effective Beat schedule is empty. Scheduled-task execution is therefore not applicable to the current application baseline.

When a periodic task is introduced, the same pull request must add a corresponding scheduling and execution contract.

## Concurrency scope

The validation confirms that concurrent duplicate executions converge safely on one persisted business result.

It does not define or certify a deployment-specific worker topology because the repository does not currently contain production orchestration settings for worker process count, pool type, autoscaling, CPU limits, or queue routing.

Those deployment settings should receive a dedicated validation when they are added to the repository.

## Guarantees

A successful check confirms:

- Celery can retry a failed task and recover;
- the production task has bounded retry configuration;
- only recognized transient dependency failures are retried;
- late acknowledgement and worker-loss rejection are enabled;
- duplicate delivery is idempotent at the GridFS persistence boundary;
- concurrent duplicate writes converge on one GridFS object;
- PostgreSQL keeps one stable `gridfs_code`;
- no scheduled-task configuration exists without a matching CI contract.

## Limits

The check does not simulate:

- an actual MongoDB or PostgreSQL outage followed by recovery;
- operating-system termination of a production worker process;
- RabbitMQ redelivery after a worker crash;
- deployment-specific prefork, gevent, eventlet, or autoscaling configuration;
- Celery Beat execution, because no schedule currently exists;
- dead-letter exchanges or poison-message handling.
