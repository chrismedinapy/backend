# Production Docker image CI validation

## Status

The repository validates its application Docker image in a dedicated GitHub Actions workflow named `Production Docker image`.

The workflow is intentionally separate from the Django integration workflow. Pull requests targeting `release` or `main` therefore expose two independent checks:

1. Django system, service integration, migration, test and coverage validation;
2. production image build and container smoke validation.

## Image baseline

The application image is built from:

```dockerfile
FROM python:3.12-slim-bookworm
```

This aligns the container runtime with the Python 3.12 version validated by the main CI pipeline. The previous Python 3.8 and Debian Buster image baseline is no longer used.

The image installs the native runtime libraries required by Django GIS/PostGIS and PostgreSQL clients, installs the pinned `requirements.txt`, runs `pip check`, and copies the application into `/app`.

## Build-context protection

The `.dockerignore` file excludes source-control metadata, GitHub workflow files, local environment files, virtual environments, caches, test reports, IDE files and runtime data.

The workflow also verifies inside the built image that the following paths are absent:

```text
/app/.git
/app/.github
/app/.env
```

This protects the image from accidentally packaging repository metadata or local credentials.

## Workflow validation

The workflow performs the following checks.

### 1. Build the real image

```bash
docker build --tag "datacore-ci:${GITHUB_SHA}" .
```

This uses the repository `Dockerfile` and real pinned dependency manifest. No alternate CI-only Dockerfile is used.

### 2. Verify image metadata and Python runtime

The workflow asserts that the image working directory is `/app`, that Python reports version 3.12, and that the installed packages pass:

```bash
python -m pip check
```

### 3. Smoke test Django and native GIS libraries

The workflow starts a disposable container and executes:

```bash
python -c "from django.contrib.gis.gdal import gdal_version; print(gdal_version())"
DJANGO_SETTINGS_MODULE=core.settings_ci python manage.py check
```

This catches images that build successfully but cannot load the native GDAL library, import the Django project, or pass Django's system checks.

## Trigger behavior

The production-image workflow runs for:

- pull requests targeting `release`;
- pull requests targeting `main`;
- pushes to `main`;
- manual `workflow_dispatch` executions.

It does not run on pushes to `release`. This avoids duplicating the image build immediately after a feature PR has already passed the same check, while retaining a post-merge validation on `main`.

## Guarantees

A successful check confirms that:

- the repository Dockerfile is syntactically valid;
- the base image and operating-system packages can be resolved;
- the pinned Python dependencies install in Python 3.12;
- dependency consistency passes inside the image;
- Django and the project settings load inside the container;
- the native GDAL integration is available;
- repository metadata and `.env` files are not copied into the image.

## Scope boundaries

This check does not prove that the complete production deployment is healthy. It does not currently validate:

- Gunicorn or another production WSGI/ASGI server;
- Kubernetes, Docker Swarm or Compose deployment manifests;
- production secrets, TLS, networking or persistent volumes;
- migrations against a production database;
- container vulnerability scanning or SBOM generation;
- multi-architecture builds;
- registry publishing or image signing.

Those capabilities should be introduced as separate, explicit release controls rather than inferred from a successful image build.
