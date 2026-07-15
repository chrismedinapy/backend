# Frontend settings and CORS

The API denies cross-origin browser access unless an origin is explicitly listed in `CORS_ALLOWED_ORIGINS`.

## Environment variables

Both CORS and CSRF values are comma-separated lists of complete origins. An origin contains the scheme, host, and optional port. Do not include paths or trailing slashes.

### Local development

```dotenv
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000
```

### Staging

```dotenv
DEBUG=False
ALLOWED_HOSTS=api-staging.example.com
CORS_ALLOWED_ORIGINS=https://app-staging.example.com
CSRF_TRUSTED_ORIGINS=https://app-staging.example.com
```

### Production

```dotenv
DEBUG=False
ALLOWED_HOSTS=api.example.com
CORS_ALLOWED_ORIGINS=https://app.example.com
CSRF_TRUSTED_ORIGINS=https://app.example.com
```

Use `CSRF_TRUSTED_ORIGINS` only for trusted browser origins that need to submit unsafe requests using cookie or session authentication. Bearer-token clients still require CORS permission in browsers, but they do not normally require CSRF trust.

## Security behavior

- `DEBUG` is parsed as a real boolean rather than a non-empty string.
- `CORS_ALLOW_ALL_ORIGINS` is always `False`.
- Missing or empty `CORS_ALLOWED_ORIGINS` produces an empty allowlist.
- `CorsMiddleware` runs before `CommonMiddleware`, as required for CORS headers to be added consistently.
- `CommonMiddleware` is registered only once.

## Validation

Run the normal checks and tests with the settings for the target environment:

```bash
python manage.py check
python manage.py test core.tests.test_settings
python manage.py check --deploy
```

`check --deploy` must be executed with production-like environment values. Review every warning before deployment, especially HTTPS redirect, secure cookies, HSTS, allowed hosts, and secret-key handling. Those controls depend on the final reverse proxy and runtime topology and must not be enabled blindly in shared base settings.
