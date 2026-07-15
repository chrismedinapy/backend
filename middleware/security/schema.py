"""OpenAPI integration for the custom bearer-token authentication class."""

from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CoreAuthenticationScheme(OpenApiAuthenticationExtension):
    """Describe CoreAuthentication as an HTTP Bearer security scheme."""

    target_class = "middleware.security.authentication.CoreAuthentication"
    name = "bearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
