from __future__ import absolute_import, unicode_literals
from decouple import config

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
REDIS_PASSWORD=config("REDIS_PASSWORD")
REDIS_HOST=config("REDIS_HOST")
REDIS_PORT=config("REDIS_PORT")
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.conf.broker_url=CELERY_BROKER_URL=f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
app.autodiscover_tasks()