# Django 5.2 LTS migration

## Status

The project CI now validates the application with Django 5.2.16 LTS on Python 3.12. The migration was validated successfully by workflow run #59.

## What changed

- Django was upgraded from 4.2.28 to 5.2.16 LTS.
- The PostGIS service used by GitHub Actions was upgraded from PostgreSQL 13 to PostgreSQL 14 because Django 5.2 requires PostgreSQL 14 or later.
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

The Django CI pipeline now validates the following stack:

- Python 3.12;
- Django 5.2.16 LTS;
- PostgreSQL 14 with PostGIS 3.2;
- Redis 7.4 cache connectivity and operations;
- dependency consistency through `pip check`;
- Django system checks;
- migration generation and application;
- the complete Django test suite;
- a minimum total coverage gate of 70%;
- `coverage.xml` publication as a workflow artifact.

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
```

Redis integration details are documented in [`docs/ci-redis.md`](ci-redis.md).

## Roadmap

- [x] Upgrade the CI runtime to Python 3.12.
- [x] Upgrade the framework to Django 5.2 LTS.
- [x] Validate Redis integration.
- [ ] Validate MongoDB integration.
- [ ] Validate RabbitMQ integration.
- [ ] Run Celery integration tests.
- [ ] Validate the production Docker image build.
