"""OpenAPI schema hooks for the public versioned API contract."""


def keep_versioned_api_endpoints(endpoints):
    """Exclude admin, docs, health and deprecated routes from generated clients."""
    return [endpoint for endpoint in endpoints if endpoint[0].startswith("/api/v1/")]
