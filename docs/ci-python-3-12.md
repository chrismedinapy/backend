# Python 3.12 CI migration

## Status

The GitHub Actions CI runtime now uses Python 3.12. The migration was validated successfully by workflow run #50.

## What changed

The migration required coordinated dependency upgrades across several areas:

- NumPy and pandas;
- compiled extensions such as cffi, psycopg2-binary, PyYAML, pyzmq, psutil and wrapt;
- Celery, billiard, kombu, amqp and vine;
- Redis and MongoDB clients;
- Django companion packages;
- linting and formatting tools;
- Jupyter and IPython tooling;
- packaging and runtime utilities.

The obsolete `backports.zoneinfo` package was removed because Python 3.12 provides `zoneinfo` in the standard library.

## Current validation

The complete dependency set installs under Python 3.12 before CI executes:

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

The CI pipeline continues to enforce the existing 70% total coverage quality gate and publishes `coverage.xml` as a workflow artifact.

## Roadmap

- [x] Upgrade the CI runtime to Python 3.12.
- [x] Modernize dependencies incompatible with Python 3.12.
- [ ] Upgrade the framework to Django 5.2 LTS.
- [ ] Validate Redis integration.
- [ ] Validate MongoDB integration.
- [ ] Validate RabbitMQ integration.
- [ ] Run Celery integration tests.
- [ ] Validate the production Docker image build.
