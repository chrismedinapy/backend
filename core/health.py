"""Lightweight service health endpoints.

These checks intentionally avoid external dependencies so they can be used by
load balancers and container orchestrators to verify that Django is serving
HTTP requests.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def healthcheck(request):
    """Return a stable JSON response when the API process is available."""
    return JsonResponse(
        {
            "status": "ok",
            "service": "datacore-api",
        }
    )
