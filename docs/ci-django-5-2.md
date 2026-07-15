# Django 5.2 LTS migration and CI baseline

## Status

The project CI validates Django 5.2.16 LTS on Python 3.12. The current baseline includes service integrations, migration checks, the deterministic Celery infrastructure healthcheck, a production asynchronous CSV-ingestion flow, retry and idempotency checks, the full Django test suite, a 70% coverage gate, and a real production Docker image build and smoke test.

Key validation milestones:

- Django 5.2 migration: workflow run #59;
- Celery infrastructure end-to-end check: workflow run #112;
- asynchronous customer-input business flow: workflow run #137;
- Celery retry and duplicate-delivery reliability: workflow run #150;
- production Docker image build and smoke test: validated by the dedicated `Production Docker image` workflow.

## What changed

- Django was upgraded from 4.2.28 to 5.2.16 LTS.
- The PostGIS service used by GitHub Actions was upgraded from PostgreSQL 13 to PostgreSQL 14 because Django 5.2 requires PostgreSQL 14 or later.
- The application Docker image was upgraded from Python 3.8 on Debian Buster to Python 3.12 on Debian Bookworm.
- The CI baseline validates one production asynchronous CSV-ingestion workflow across the API, PostgreSQL/PostGIS, filesystem storage, RabbitMQ, Celery, and MongoDB GridFS.
- The production CSV-ingestion task has bounded retries for transient dependency failures, late acknowledgement, and worker-loss rejection.
- GridFS persistence uses a deterministic identifier so duplicate deliveries converge on one business result.
- The production Docker image is built from the repository `Dockerfile` and smoke-tested with Python, dependency, Django, and GDAL checks.
- No additional Django application compatibility changes were required after reviewing removals and deprecations from Django 5.0, 5.1, and 5.2.

## Compatibility review

The repository was reviewed for common Django 5.x incompatibilities, including:

- removed legacy URL helpers;
- deprecated GIS admin classes;
- obsolete localization and timezone settings;
- direct `pytz` usage;
- middleware and settings incompatibilities;
- migration compatibility with the supported PostgreSQL baseline.

No direct application usages requiring additional compatibility changes were found during the migration.

## Current CI model

Pull requests targeting `release` or `main` expose two complementary checks:

1. `Django system, migration, test and coverage checks`;
2. `Build and smoke test production image`.

The first validates the application and service contracts. The second validates the deployable container artifact.

Together they validate:

- Python 3.12;
- Django 5.2.16 LTS;
- PostgreSQL 14 with PostGIS 3.2;
- Redis 7.4 cache connectivity and operations;
- MongoDB 8.0 connectivity and CRUD operations;
- RabbitMQ authentication and AMQP connectivity through the real Celery broker configuration;
- deterministic Celery publication, queue consumption, worker execution, and Redis execution-marker validation;
- a deterministic Celery retry that fails once and recovers on the second execution;
- bounded transient retry configuration on the production `create_collection` task;
- late acknowledgement and worker-loss rejection on the production task;
- an authenticated multipart request through the real CSV-ingestion endpoint;
- PostgreSQL/PostGIS metadata persistence;
- uploaded-file persistence;
- publication and execution of the production `create_collection` task;
- MongoDB GridFS persistence;
- deterministic GridFS identifiers for duplicate delivery;
- four concurrent persistence calls converging on one GridFS object;
- propagation of the stable GridFS identifier back into PostgreSQL;
- exact persisted-data assertions and cleanup;
- an explicit assertion that no Celery Beat schedule exists without a matching CI contract;
- dependency consistency through `pip check`;
- Django system checks;
- missing-migration detection and migration application;
- the complete Django test suite;
- a minimum total coverage gate of 70%;
- `coverage.xml` publication as a workflow artifact;
- conditional worker and business-flow diagnostics on failure;
- production Docker image construction from the real repository `Dockerfile`;
- Python, dependency, Django, and native GDAL smoke checks inside the image;
- exclusion of `.git`, `.github`, and `.env` from the final image.

## Validation commands

```bash
python -m pip check
python manage.py check
python manage.py makemigrations --dry-run --verbosity 3
python manage.py migrate --noinput --verbosity=1
python manage.py showmigrations --plan
python scripts/ci/validate_async_customer_input_flow.py
coverage run --source=core,data,middleware manage.py test --verbosity=2
coverage report --show-missing --fail-under=70
coverage xml

docker build --tag datacore-ci:local .
docker run --rm datacore-ci:local python -m pip check
docker run --rm \
  --env DJANGO_SETTINGS_MODULE=core.settings_ci \
  datacore-ci:local \
  python manage.py check
```

## Related documentation

- [Redis integration](ci-redis.md)
- [MongoDB integration](ci-mongodb.md)
- [RabbitMQ integration](ci-rabbitmq.md)
- [Celery infrastructure integration](ci-celery.md)
- [Celery retries, idempotency, and concurrency](ci-celery-reliability.md)
- [Asynchronous customer-input business flow](ci-async-business-flow.md)
- [Production Docker image validation](ci-docker-image.md)

## Roadmap

Completed:

- [x] Upgrade the CI runtime to Python 3.12.
- [x] Upgrade the framework to Django 5.2 LTS.
- [x] Validate Redis integration.
- [x] Validate MongoDB integration.
- [x] Validate RabbitMQ integration through Celery configuration.
- [x] Run an end-to-end Celery worker and deterministic task integration test.
- [x] Validate the production Docker image build and container smoke test.
- [x] Add an application-specific asynchronous business-flow integration test.
- [x] Validate bounded retries and transient-failure classification.
- [x] Validate idempotency and duplicate-delivery behavior.
- [x] Validate concurrent duplicate persistence at the shared GridFS boundary.
- [x] Review scheduled-task scope and assert that no Beat schedule is currently configured.

Next:

- [ ] Add image vulnerability scanning, SBOM generation, registry publishing, and signing where required.
- [ ] Validate deployment-specific worker pool and autoscaling settings when production orchestration is added to the repository.
