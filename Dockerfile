FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.title="DataCore" \
      org.opencontainers.image.description="Django REST backend for DataCore"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=core.settings_production \
    PORT=8000

WORKDIR /app

# Runtime libraries required by Django GIS/PostGIS and PostgreSQL clients.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        gdal-bin \
        libgdal-dev \
        libgeos-c1v5 \
        libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app \
    && useradd --system --gid app --home-dir /app app

COPY requirements.txt requirements-runtime.txt ./

RUN python -m pip install --upgrade \
        "pip==24.3.1" \
        "setuptools<76" \
        "wheel<0.46" \
    && python -m pip install -r requirements-runtime.txt \
    && python -m pip check

COPY --chown=app:app . /app/

# Django creates and writes runtime files below FILES_ROOT. Keep the image
# non-root while explicitly granting ownership only to application paths.
RUN mkdir -p /app/files \
    && chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '8000') + '/api/v1/health/', timeout=3)"

CMD ["gunicorn", "core.wsgi:application", "--config", "python:gunicorn.conf"]
