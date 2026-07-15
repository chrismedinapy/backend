"""Root URL configuration for the DataCore service."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core.health import healthcheck
from data.routes import routes_backoffice


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
    path("api/v1/health/", healthcheck, name="api-v1-healthcheck"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-redoc",
    ),
    path("api/v1/data/", include(routes_backoffice)),
    # Deprecated compatibility route. Remove only after existing clients have
    # migrated to /api/v1/data/.
    path("data/", include(routes_backoffice)),
]
