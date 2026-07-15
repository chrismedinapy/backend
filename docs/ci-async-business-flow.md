# Asynchronous customer-input business-flow validation

## Status

The `Django CI baseline` workflow validates one real asynchronous application flow in addition to the lower-level Celery infrastructure healthcheck.

The first successful end-to-end business-flow validation completed in Django CI workflow run #137.

## Business path under test

The check exercises the production CSV-ingestion contract:

```text
Authenticated multipart HTTP POST
→ CustomerInput metadata persisted in PostgreSQL/PostGIS
→ uploaded CSV persisted on the application filesystem
→ data.task.create_customer_input_dataset.create_collection published to RabbitMQ
→ separate Celery worker consumes and executes the production task
→ parsed dataset persisted in MongoDB GridFS
→ GridFS identifier persisted back to CustomerInput.gridfs_code in PostgreSQL
→ exact PostgreSQL and MongoDB assertions
→ generated records, GridFS object and file removed
```

This is an application-specific end-to-end test. It complements the deterministic `core.ci_healthcheck` test, which isolates the Celery, RabbitMQ and Redis infrastructure contract.

## Endpoint and authentication

The validation script calls the real endpoint:

```text
POST /data/customers/<customer_code>/retail-store/<retail_store_code>/products/
```

The request uses multipart form data containing:

- the JSON customer-input description;
- a generated CSV file;
- a short-lived JWT for a temporary CI user.

The endpoint is invoked through Django REST Framework's `APIClient`. The view, authentication class, serializers, validators and production business logic are therefore exercised rather than bypassed.

## Temporary business fixtures

The script creates unique temporary records for:

- `User`;
- `Customer`;
- `RetailStore`;
- `CustomerInput` through the real endpoint.

UUIDs and identifying values are generated at runtime. No production credentials or reusable passwords are stored in the repository.

The temporary CSV contains a small deterministic dataset so the final GridFS content can be asserted exactly.

## Celery task registration

Celery's Django autodiscovery searches installed applications for a `tasks.py` module. The existing production task implementation remains in:

```text
data/task/create_customer_input_dataset.py
```

The application now exposes `data/tasks.py`, which re-exports `create_collection`. This ensures a normal worker startup registers the production task without requiring CI-only `--include` arguments.

## MongoDB configuration

The production MongoDB client now honors:

```text
MONGO_HOST
MONGO_PORT
MONGO_INITDB_DATABASE
```

The previous hard-coded `mongodb:27017` address prevented the production task from working in environments where the database service is reached through another hostname, including GitHub Actions service-port mappings.

## Workflow execution

The business-flow stage runs after migrations and before the Django test suite. GitHub Actions starts a separate worker with:

```bash
celery -A core.celery:app worker \
  --pool=solo \
  --concurrency=1 \
  --loglevel=WARNING \
  --without-gossip \
  --without-mingle \
  --without-heartbeat
```

The validation script is then executed:

```bash
python scripts/ci/validate_async_customer_input_flow.py
```

The script adds the repository root to its import path, so it can load `core.settings_ci` reliably when invoked directly.

## Assertions

A successful stage confirms all of the following:

- JWT authentication accepts the generated CI identity;
- the multipart endpoint returns HTTP `201`;
- a `CustomerInput` record is created in PostgreSQL;
- the CSV hash and filesystem location are persisted;
- the uploaded file exists;
- the real production Celery task is registered and published through RabbitMQ;
- a separate worker consumes and executes the task;
- the dataset is written to MongoDB GridFS;
- `CustomerInput.gridfs_code` is updated by the worker;
- the GridFS payload contains the expected columns and rows.

## Cleanup

The script removes all generated state in a `finally` block:

- Redis cache entries are cleared;
- the GridFS object is deleted;
- temporary PostgreSQL records are deleted;
- the generated CSV directory is removed;
- database connections are closed.

Cleanup warnings do not hide the original validation failure.

## Failure diagnostics

The worker writes to:

```text
/tmp/celery-business-worker.log
```

The validation script output and traceback are written to:

```text
/tmp/async-business-flow.log
```

The `Upload asynchronous business-flow diagnostics` stage uses `if: failure()` and uploads both files as the `async-business-flow-diagnostics` artifact. It is expected to appear as `skipped` on a successful workflow.

## Guarantees

A green check provides strong regression protection for the tested CSV-ingestion contract across:

- Django REST endpoint routing and request handling;
- authentication and validation;
- PostgreSQL/PostGIS persistence;
- application file storage;
- Celery production-task registration;
- RabbitMQ publication and delivery;
- separate worker execution;
- MongoDB GridFS persistence;
- cross-database state propagation.

## Scope boundaries

The check validates one representative production workflow. It does not currently prove:

- retry behavior after transient failures;
- idempotency or duplicate message delivery handling;
- acknowledgements, dead-letter queues or task rejection behavior;
- Celery Beat or scheduled tasks;
- multiple workers or production concurrency pools;
- large-file performance and resource limits;
- complete production container orchestration, networking or secrets;
- every asynchronous task or API endpoint in the application.

Those concerns should remain separate, explicit controls rather than being inferred from this single successful flow.