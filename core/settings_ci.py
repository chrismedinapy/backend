"""Settings used by automated CI checks.

This module provides deterministic, non-production defaults before importing the
normal project settings. Real CI environment variables may override any value.
"""

import os


CI_DEFAULTS = {
    "SECRET_KEY": "ci-not-a-real-secret",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_DAYS": "1",
    "ENCODING": "utf-8",
    "DEBUG": "False",
    "CELERY_DEBUG": "False",
    "ALLOWED_HOSTS": "localhost,127.0.0.1",
    "CORS_ALLOWED_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000",
    "CSRF_TRUSTED_ORIGINS": "http://localhost:3000",
    "DJANGO_PORT": "8000",
    "ADMINER_PORT": "8080",
    "POSTGRES_DB": "core_test",
    "POSTGRES_USER": "core",
    "POSTGRES_PASSWORD": "core",
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": "5432",
    "POSTGRES_HOST_AUTH_METHOD": "trust",
    "REDIS_HOST": "localhost",
    "REDIS_PORT": "6379",
    "REDIS_PASSWORD": "",
    "MONGO_INITDB_DATABASE": "core_test",
    "MONGO_HOST": "localhost",
    "MONGO_PORT": "27017",
    "ME_CONFIG_BASICAUTH_USERNAME": "ci",
    "ME_CONFIG_BASICAUTH_PASSWORD": "ci",
    "ME_CONFIG_MONGODB_SERVER": "localhost",
    "RABBITMQ_DEFAULT_HOST": "localhost",
    "RABBITMQ_PORTS_1": "5672",
    "RABBITMQ_PORTS_2": "15672",
    "RABBITMQ_DEFAULT_USER": "core",
    "RABBITMQ_DEFAULT_PASS": "core",
    "RABBITMQ_DEFAULT_VHOST": "/",
}

for variable, default_value in CI_DEFAULTS.items():
    os.environ.setdefault(variable, default_value)

from .settings import *  # noqa: E402,F401,F403


DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# RabbitMQ remains the broker used by the application. Redis database 1 is an
# isolated result backend used only to prove end-to-end task execution in CI.
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_EXPIRES = 300

# RabbitMQ 4 rejects the deprecated transient non-exclusive queue used by
# Celery's remote-control pidbox. The CI task test does not use inspect, ping,
# broadcast, revoke, or other remote-control commands, so disable that optional
# worker subsystem only in the isolated CI settings.
CELERY_WORKER_ENABLE_REMOTE_CONTROL = False

# The project package is not a Django application, so Celery autodiscovery does
# not scan it. Import the deterministic CI-only task explicitly for the worker.
CELERY_IMPORTS = ("core.ci_tasks",)
