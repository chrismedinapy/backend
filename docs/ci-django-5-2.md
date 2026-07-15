# Django 5.2 LTS migration

## Status

The project CI validates the application with Django 5.2.16 LTS on Python 3.12. The Django migration was validated successfully by workflow run #59. The infrastructure baseline, including the end-to-end Celery subsystem check, was validated successfully by workflow run #112. The production Docker image build and container smoke test were first validated successfully by the `Production Docker image` workflow run #1.

## What changed

- Django was upgraded from 4.2.28 to 5.2.16 LTS.
- The PostGIS service used by GitHub Actions was upgraded from PostgreSQL 13 to PostgreSQL 14 because Django 5.2 requires PostgreSQL 14 or later.
- The application Docker image was upgraded from Python 3.8 on Debian Buster to Python 3.12 on Debian Bookworm.
- No application-level compatibility changes were required after reviewing common removals and deprecations from Django 5.0, 5.1 and 5.2.
- Temporary diagnostic workflow changes and unrelated UUID migration changes were removed before the final validation.

## Compatibility review

The repository was reviewed for common Django 5.x incompatibilities, including:

- removed legacy URL helpers;
- deprecated GIS admin classes;
- obsolete localization and timezone settings;
- direct `pytz` usage;
- middleware and settings incompatibilities;
- migration compatibility with the supported PostgreSQL baseline.

No direct application usages requiring code changes were found during the migration.

## Current CI baseline

The repository CI validates the following stack:

- Python 3.12;
- Django 5.2.16 LTS;
- PostgreSQL 14 with PostGIS 3.2;
- Redis 7.4 cache connectivity and operations;
- MongoDB 8.0 connectivity and CRUD operations;
- RabbitMQ authentication and AMQP connectivity through the real Celery broker configuration;
- end-to-end Celery task publication, queue consumption, worker execution and Redis execution-marker validation;
- dependency consistency through `pip check`;
- Django system checks;
- migration generation and application;
- the complete Django test suite;
- a minimum total coverage gate of 70%;
- `coverage.xml` publication as a workflow artifact;
- conditional Celery worker diagnostics when the job fails;
- production Docker image construction from the real repository `Dockerfile`;
- Python, dependency, Django and native GDAL smoke checks inside the built image;
- verification that `.git`, `.github` and `.env` are excluded from the image.

The Celery check is an end-to-end test of the asynchronous infrastructure subsystem. It does not replace application-specific tests for production tasks or complete HTTP-to-database business workflows.

The Docker check validates image construction and application startup prerequisites. It does not replace deployment, registry, security-scanning or production-network validation.

## Validation commands

```bash
python -m pip check
python manage.py check
python manage.py makemigrations --dry-run --verbosity 3
python manage.py migrate --noinput --verbosity=1
python manage.py showmigrations --plan
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

Redis integration details are documented in [`docs/ci-redis.md`](ci-redis.md).
MongoDB integration details are documented in [`docs/ci-mongodb.md`](ci-mongodb.md).
RabbitMQ integration details are documented in [`docs/ci-rabbitmq.md`](ci-rabbitmq.md).
Celery integration details, coverage boundaries and RabbitMQ 4 compatibility are documented in [`docs/ci-celery.md`](ci-celery.md).
Production image build, smoke-test guarantees and scope boundaries are documented in [`docs/ci-docker-image.md`](ci-docker-image.md).

## Roadmap

- [x] Upgrade the CI runtime to Python 3.12.
- [x] Upgrade the framework to Django 5.2 LTS.
- [x] Validate Redis integration.
- [x] Validate MongoDB integration.
- [x] Validate RabbitMQ integration through Celery configuration.
- [x] Run an end-to-end Celery worker and task integration test.
- [x] Validate the production Docker image build and container smoke test.
- [ ] Add an application-specific asynchronous business-flow integration test.
- [ ] Add image vulnerability scanning, SBOM generation, registry publishing and signing where required.
