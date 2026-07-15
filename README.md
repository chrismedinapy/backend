# DataCore

DataCore is a Django REST backend for ingesting CSV files, storing relational metadata in PostgreSQL/PostGIS, persisting tabular datasets in MongoDB, caching application data in Redis, and processing asynchronous workloads through Celery and RabbitMQ.

## Contents

- [Project overview](#project-overview)
- [Architecture](#architecture)
- [Technology baseline](#technology-baseline)
- [Development setup](#development-setup)
- [Continuous integration](#continuous-integration)
- [Branch and release workflow](#branch-and-release-workflow)
- [Technical documentation](#technical-documentation)
- [Current roadmap](#current-roadmap)
- [Diagrams](#diagrams)

## Project overview

The project models a retail analytics service. A client uploads CSV data, the application records metadata in PostgreSQL/PostGIS, stores the extracted tabular data in MongoDB GridFS, and schedules processing through Celery and RabbitMQ. Redis provides caching and an isolated execution marker for the lower-level Celery CI healthcheck.

The application flow includes:

1. user and customer management;
2. CSV upload and duplicate detection;
3. metadata persistence in PostgreSQL/PostGIS;
4. file persistence on the configured application storage;
5. asynchronous publication through Celery and RabbitMQ;
6. tabular dataset persistence in MongoDB GridFS;
7. cached reads through Redis;
8. reporting and clustering workflows.

## Architecture

```text
Django REST API
├── PostgreSQL 14 + PostGIS 3.2   relational metadata and GIS data
├── MongoDB 8.0                   datasets and GridFS objects
├── Redis 7.4                     application cache and CI execution markers
└── Celery 5.4
    └── RabbitMQ 4                asynchronous task broker
```

The CI baseline validates the application and its service integrations, exercises both a deterministic Celery infrastructure healthcheck and a real asynchronous CSV-ingestion flow, and builds and smoke-tests the production Docker image.

## Technology baseline

| Component | Validated version or role |
| --- | --- |
| Python | 3.12 |
| Django | 5.2.16 LTS |
| Django REST Framework | 3.15.2 |
| PostgreSQL/PostGIS | PostgreSQL 14 with PostGIS 3.2 |
| MongoDB | 8.0 |
| Redis | 7.4 |
| RabbitMQ | 4.x |
| Celery | 5.4.0 |
| Application image | Python 3.12 slim on Debian Bookworm |
| Coverage gate | Minimum 70% total measured coverage |
| CI runner | Ubuntu 22.04 |

The complete pinned Python dependency set is maintained in [`requirements.txt`](requirements.txt).

## Development setup

### 1. Clone the repository

```bash
git clone https://github.com/chrismedinapy/backend.git
cd backend
```

### 2. Create a Python environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

### 3. Configure environment variables

Create a `.env` file in the repository root. The application settings expect values equivalent to:

```dotenv
SECRET_KEY=<required>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=core
POSTGRES_USER=core
POSTGRES_PASSWORD=<required>
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

MONGO_INITDB_DATABASE=data
MONGO_HOST=localhost
MONGO_PORT=27017

RABBITMQ_DEFAULT_HOST=localhost
RABBITMQ_PORTS_1=5672
RABBITMQ_PORTS_2=15672
RABBITMQ_DEFAULT_USER=core
RABBITMQ_DEFAULT_PASS=<required>
RABBITMQ_DEFAULT_VHOST=/

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=1
ENCODING=utf-8
DJANGO_PORT=8000
ADMINER_PORT=8080
CELERY_DEBUG=False
```

Do not commit real credentials or local `.env` files.

### 4. Prepare and run Django

With PostgreSQL/PostGIS, Redis, MongoDB, and RabbitMQ available at the configured addresses:

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

The isolated CI configuration can be checked locally with:

```bash
DJANGO_SETTINGS_MODULE=core.settings_ci python manage.py check
```

### 5. Build and smoke-test the production image

```bash
docker build --tag datacore:local .
docker run --rm datacore:local python -m pip check
docker run --rm \
  --env DJANGO_SETTINGS_MODULE=core.settings_ci \
  datacore:local \
  python manage.py check
```

The automated image workflow confirms that the real repository `Dockerfile` builds, uses Python 3.12, loads the native GDAL integration, passes dependency and Django checks, and excludes `.git`, `.github`, and `.env` from the final image.

This image check does not yet validate the complete deployment topology, registry publication, image signing, vulnerability scanning, or production networking and secrets.

## Continuous integration

Two complementary GitHub Actions workflows protect pull requests targeting `release` or `main`:

1. `Django CI baseline` validates the application, migrations, service integrations, asynchronous flows, tests, and coverage.
2. `Production Docker image` builds and smoke-tests the application container.

A normal pull request is expected to show these two primary checks:

```text
Django system, migration, test and coverage checks
Build and smoke test production image
```

They are intentionally separate. One validates the application and service contracts; the other validates the deployable container artifact.

The Django workflow runs for pull requests and pushes targeting `release` and `main`. The image workflow runs for pull requests targeting `release` or `main`, pushes to `main`, and manual executions. It intentionally skips pushes to `release` to avoid repeating a successful PR image build immediately after merge.

The application checks use:

```text
DJANGO_SETTINGS_MODULE=core.settings_ci
```

### Current CI validation

The baseline currently validates:

- dependency installation and consistency through `pip check`;
- Django system checks;
- PostgreSQL/PostGIS connectivity;
- missing-migration detection;
- migration application and migration-plan generation;
- Redis connectivity and cache operations;
- MongoDB connectivity and CRUD operations;
- RabbitMQ authentication and AMQP connectivity through the real Celery configuration;
- deterministic Celery task publication, broker delivery, worker execution, and Redis marker assertion;
- an authenticated multipart CSV upload through the production API;
- `CustomerInput` metadata persistence in PostgreSQL/PostGIS;
- CSV persistence on the application filesystem;
- publication and execution of the production `create_collection` Celery task;
- dataset persistence in MongoDB GridFS;
- propagation of `gridfs_code` back into PostgreSQL;
- exact persisted-data assertions and cleanup of generated records, files, and GridFS objects;
- the complete Django test suite;
- a minimum total coverage gate of 70%;
- publication of `coverage.xml` as a workflow artifact;
- conditional publication of Celery and asynchronous-flow diagnostics on failure;
- construction of the real application Docker image;
- Python, dependency, Django, and native GDAL smoke checks inside the image;
- exclusion of repository metadata and local environment files from the image.

Core validation commands include:

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
```

### Celery infrastructure healthcheck

The deterministic infrastructure check exercises:

```text
core.settings_ci
→ core.celery.app
→ RabbitMQ
→ separate Celery worker
→ core.ci_healthcheck
→ Redis database 1 execution marker
→ exact marker assertion
```

This gives focused regression protection for the Celery, RabbitMQ, and Redis infrastructure contract.

`Upload Celery worker diagnostics` runs only after a failure. Seeing it as `skipped` on a successful workflow is expected.

### Asynchronous business-flow check

The application-specific test exercises:

```text
Authenticated multipart HTTP POST
→ PostgreSQL/PostGIS metadata
→ application file storage
→ RabbitMQ publication
→ separate Celery worker
→ production create_collection task
→ MongoDB GridFS dataset
→ PostgreSQL gridfs_code update
→ exact assertions and cleanup
```

This verifies a real production business contract rather than only a synthetic healthcheck. It still does not cover every task, failure mode, retry policy, or concurrency topology.

### Production image check

The container workflow exercises:

```text
Dockerfile
→ python:3.12-slim-bookworm
→ native GIS and PostgreSQL libraries
→ requirements.txt installation
→ pip check
→ Django GIS/GDAL import
→ manage.py check inside the image
→ sensitive-path exclusion assertions
```

A successful image check means the repository can produce a runnable application image with the validated runtime and native dependencies. It does not independently certify the complete production deployment.

## Branch and release workflow

The repository uses two permanent branches:

```text
feature/*
    ↓ pull request
release
    ↓ promotion pull request
main
```

- `feature/*` branches contain focused changes.
- `release` is the integration and release-candidate branch.
- `main` contains promoted and reviewed releases.
- Changes integrated independently into `main` must be synchronized back into `release` before the next promotion.
- Both application and production-image checks must pass before promotion between permanent branches.

## Technical documentation

Detailed CI notes are maintained in the `docs` directory:

- [Django 5.2 LTS and CI baseline](docs/ci-django-5-2.md)
- [Redis integration](docs/ci-redis.md)
- [MongoDB integration](docs/ci-mongodb.md)
- [RabbitMQ integration](docs/ci-rabbitmq.md)
- [Celery infrastructure end-to-end integration](docs/ci-celery.md)
- [Asynchronous customer-input business flow](docs/ci-async-business-flow.md)
- [Production Docker image validation](docs/ci-docker-image.md)

These documents describe the tested architecture, settings, assertions, diagnostics, guarantees, trigger behavior, and scope boundaries.

## Current roadmap

Completed:

- [x] Python 3.12 CI runtime;
- [x] Django 5.2 LTS migration;
- [x] PostgreSQL 14/PostGIS migration validation;
- [x] Redis integration checks;
- [x] MongoDB integration checks;
- [x] RabbitMQ connectivity through Celery configuration;
- [x] Celery worker and deterministic task end-to-end integration;
- [x] dependency consistency validation;
- [x] migration integrity checks;
- [x] Django test suite and 70% coverage gate;
- [x] failure diagnostics and workflow artifacts;
- [x] production Docker image build and container smoke test;
- [x] application-specific asynchronous business-flow integration test.

Next:

- [ ] validate retries, idempotency, scheduled tasks, and production worker concurrency where required;
- [ ] add container vulnerability scanning and SBOM generation where required;
- [ ] add registry publishing and image signing where required.

## Diagrams

### CSV upload flow

![User uploads a CSV file](diagram-images/user-save-csv.png)

1. The user uploads a CSV file through the API.
2. The service generates and checks a file hash to prevent duplicate uploads.
3. File and user metadata are stored in PostgreSQL/PostGIS.
4. The CSV file is persisted to the configured file storage.
5. Celery publishes an asynchronous task through RabbitMQ.
6. A worker extracts the data frame and stores the tabular data in MongoDB GridFS.
7. The GridFS identifier is persisted back into PostgreSQL/PostGIS.

### Report request flow

![User requests a report](diagram-images/user-request-new-report.png)

1. The user requests a report.
2. The API checks Redis for cached data.
3. A Celery task is published to RabbitMQ when processing is required.
4. A worker loads relational metadata and the corresponding MongoDB data frames.
5. The worker performs the reporting or clustering workflow.
6. Results and status information are persisted and returned through the application flow.
