"""Contract tests for the public OpenAPI and documentation endpoints."""

import yaml
from django.test import TestCase
from django.urls import reverse


class OpenAPIDocumentationTests(TestCase):
    """Exercise schema generation against the real Django URL and model setup."""

    def _schema(self):
        response = self.client.get(reverse("api-schema"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response["Content-Type"].startswith("application/vnd.oai.openapi"),
            response["Content-Type"],
        )
        return yaml.safe_load(response.content)

    def test_schema_endpoint_returns_valid_openapi_document(self):
        schema = self._schema()

        self.assertEqual(schema["openapi"], "3.0.3")
        self.assertEqual(schema["info"]["title"], "DataCore API")
        self.assertEqual(schema["info"]["version"], "1.0.0")
        self.assertIn("paths", schema)

    def test_schema_documents_bearer_jwt_authentication(self):
        schema = self._schema()
        bearer = schema["components"]["securitySchemes"]["bearerAuth"]

        self.assertEqual(bearer["type"], "http")
        self.assertEqual(bearer["scheme"], "bearer")
        self.assertEqual(bearer["bearerFormat"], "JWT")

    def test_schema_contains_versioned_api_paths_only(self):
        schema = self._schema()
        documented_paths = schema["paths"]

        self.assertTrue(documented_paths)
        self.assertTrue(all(path.startswith("/api/v1/") for path in documented_paths))
        self.assertFalse(any(path.startswith("/data/") for path in documented_paths))

    def test_swagger_ui_is_available(self):
        response = self.client.get(reverse("api-docs"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("api-schema"))

    def test_redoc_ui_is_available(self):
        response = self.client.get(reverse("api-redoc"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("api-schema"))
