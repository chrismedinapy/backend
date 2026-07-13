"""Settings used by automated CI checks.

This module provides deterministic, non-production defaults before importing the
normal project settings. Real CI environment variables may override any value.
"""

import os


CI_DEFAULTS = {
    "SECRET_KEY": "ci-not-a-real-secret",
    "DEBUG": "False",
    "ALLOWED_HOSTS": "localhost,127.0.0.1",
    "POSTGRES_DB": "core_test",
    "POSTGRES_USER": "core",
    "POSTGRES_PASSWORD": "core",
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": "5432",
    "REDIS_HOST": "localhost",
    "REDIS_PORT": "6379",
    "REDIS_PASSWORD": "ci-redis-password",
    "RABBITMQ_DEFAULT_HOST": "localhost",
    "RABBITMQ_PORTS_1": "5672",
    "RABBITMQ_DEFAULT_USER": "core",
    "RABBITMQ_DEFAULT_PASS": "core",
    "RABBITMQ_DEFAULT_VHOST": "/",
    "ACCESS_TOKEN_EXPIRE_DAYS": "1",
    "ALGORITHM": "HS256",
}

for variable, default_value in CI_DEFAULTS.items():
    os.environ.setdefault(variable, default_value)

from .settings import *  # noqa: E402,F401,F403


DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
