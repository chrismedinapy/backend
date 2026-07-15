"""Gunicorn configuration for the production API runtime."""

import multiprocessing
import os


def env_int(name, default):
    value = int(os.getenv(name, default))
    if value < 1:
        raise ValueError(f"{name} must be greater than zero")
    return value


bind = f"0.0.0.0:{env_int('PORT', 8000)}"
workers = env_int("GUNICORN_WORKERS", max(2, multiprocessing.cpu_count() * 2 + 1))
threads = env_int("GUNICORN_THREADS", 1)
timeout = env_int("GUNICORN_TIMEOUT", 30)
graceful_timeout = env_int("GUNICORN_GRACEFUL_TIMEOUT", 30)
keepalive = env_int("GUNICORN_KEEPALIVE", 5)
worker_tmp_dir = "/dev/shm"
accesslog = "-"
errorlog = "-"
capture_output = True
forwarded_allow_ips = os.getenv("GUNICORN_FORWARDED_ALLOW_IPS", "127.0.0.1")
