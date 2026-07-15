"""
Django settings for the core project.
"""
import os
from pathlib import Path

from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent


def csv_list(value):
    """Convert a comma-separated environment value into a clean list."""
    return [item.strip() for item in value.split(",") if item.strip()]


SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=csv_list)

# Cross-origin access is deny-by-default. Each environment must explicitly
# provide the frontend origins allowed to call this API.
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="",
    cast=csv_list,
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="",
    cast=csv_list,
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "data",
    "middleware",
    "django.contrib.gis",
    "rest_framework_gis",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middleware.errors.error_handler.CoreErrorMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "middleware.security.authentication.CoreAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "middleware.security.permission.CorePermission",
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_PAGINATION_CLASS": "data.utils.paginator.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "middleware.errors.api_errors.api_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "DataCore API",
    "DESCRIPTION": (
        "Versioned HTTP API for DataCore. New frontend integrations must use "
        "the /api/v1/ routes."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v1",
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": True,
    "PREPROCESSING_HOOKS": ["core.schema.keep_versioned_api_endpoints"],
}

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "core.wsgi.application"

REDIS_PASSWORD = config("REDIS_PASSWORD", default="")
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT")
REDIS_LOCATION = (
    f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
    if REDIS_PASSWORD
    else f"redis://{REDIS_HOST}:{REDIS_PORT}"
)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_LOCATION,
    }
}

REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_CACHE_RESPONSE_TIMEOUT": 60 * 60 * 2,
}

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
FILES_ROOT = os.path.join(BASE_DIR, "files")

if not os.path.exists(FILES_ROOT):
    os.makedirs(FILES_ROOT)

FILES_URL = "files/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

PROTOCOL = ("amqp",)
RABBITMQ_HOST = config("RABBITMQ_DEFAULT_HOST")
RABBITMQ_PORT = config("RABBITMQ_PORTS_1")
RABBITMQ_USER = config("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = config("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_HOST = config("RABBITMQ_DEFAULT_HOST")
RABBITMQ_DEFAULT_VHOST = config("RABBITMQ_DEFAULT_VHOST")

CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@"
    f"{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_DEFAULT_VHOST}"
)
