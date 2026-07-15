FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.title="DataCore" \
      org.opencontainers.image.description="Django REST backend for DataCore"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Runtime libraries required by Django GIS/PostGIS and PostgreSQL clients.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        gdal-bin \
        libgdal-dev \
        libgeos-c1v5 \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN python -m pip install --upgrade \
        "pip==24.3.1" \
        "setuptools<76" \
        "wheel<0.46" \
    && python -m pip install -r requirements.txt \
    && python -m pip check

COPY . /app/

EXPOSE 8000
