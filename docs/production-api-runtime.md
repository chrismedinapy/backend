# Production API runtime

The production image starts the Django WSGI application with Gunicorn and uses `core.settings_production`.

## Runtime behavior

- Gunicorn is PID 1 and receives container termination signals directly.
- The application runs as the non-root `app` user.
- Access and error logs are written to stdout and stderr.
- Django application logs are JSON and include `request_id`.
- The API accepts a valid `X-Request-ID` header or generates one and returns it in the response.
- Docker checks `/api/v1/health/` on the internal application port.

## Gunicorn variables

- `PORT`, default `8000`
- `GUNICORN_WORKERS`, default based on available CPUs
- `GUNICORN_THREADS`, default `1`
- `GUNICORN_TIMEOUT`, default `30`
- `GUNICORN_GRACEFUL_TIMEOUT`, default `30`
- `GUNICORN_KEEPALIVE`, default `5`
- `GUNICORN_FORWARDED_ALLOW_IPS`, default `127.0.0.1`

All numeric runtime values must be greater than zero. Set `GUNICORN_FORWARDED_ALLOW_IPS` only to trusted reverse-proxy addresses or networks.

## Proxy and HTTPS variables

Production settings trust `X-Forwarded-Proto: https` only after Gunicorn accepts the forwarding proxy. The following switches default to secure values:

- `USE_X_FORWARDED_HOST=True`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SECURE_HSTS_SECONDS=3600`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- `SECURE_HSTS_PRELOAD=False`

Do not enable HSTS preload until every relevant subdomain is permanently HTTPS-ready.

## Logging variables

- `LOG_LEVEL`, default `INFO`
- `DJANGO_LOG_LEVEL`, default `INFO`

Logs are emitted as one JSON object per line with timestamp, level, logger, message, and request ID.

## Deployment validation

Run production checks with production-like environment values:

```bash
DJANGO_SETTINGS_MODULE=core.settings_production python manage.py check --deploy
```

Build and run the same image used in production. The platform should wait for the container healthcheck before routing traffic and allow at least `GUNICORN_GRACEFUL_TIMEOUT` seconds during termination.
