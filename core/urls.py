"""Root URL configuration for the DataCore service."""

from django.contrib import admin
from django.urls import include, path

from core.health import healthcheck
from data.routes import routes_backoffice


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("api/v1/health/", healthcheck, name="api-v1-healthcheck"),
    path("api/v1/data/", include(routes_backoffice)),
    # Deprecated compatibility route. Remove only after existing clients have
    # migrated to /api/v1/data/.
    path("data/", include(routes_backoffice)),
]
