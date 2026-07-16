"""Tests for the stable frontend-facing API error contract."""

import json

from django.test import RequestFactory, SimpleTestCase
from rest_framework.exceptions import (
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    UnsupportedMediaType,
    ValidationError,
)

from data.utils.exceptions import DuplicatedRecord, InvalidToken
from middleware.errors.api_errors import api_exception_handler
from middleware.errors.error_handler import CoreErrorMiddleware


class APIExceptionHandlerTests(SimpleTestCase):
    def _handle(self, exception):
        response = api_exception_handler(exception, {"view": None, "request": None})
        self.assertIsNotNone(response)
        return response

    def assert_error(self, response, status_code, code, message=None, fields=None):
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(set(response.data), {"error"})
        self.assertEqual(response.data["error"]["code"], code)
        if message is not None:
            self.assertEqual(response.data["error"]["message"], message)
        self.assertEqual(response.data["error"]["fields"], fields or {})

    def test_validation_error_includes_field_errors(self):
        response = self._handle(
            ValidationError({"email": ["Enter a valid email address."]})
        )

        self.assert_error(
            response,
            400,
            "invalid_parameter",
            "Invalid parameter",
            {"email": ["Enter a valid email address."]},
        )

    def test_not_authenticated_uses_stable_401_contract(self):
        response = self._handle(NotAuthenticated("Credentials were not provided."))

        self.assert_error(
            response,
            401,
            "authentication_required",
            "Credentials were not provided.",
        )

    def test_legacy_invalid_token_maps_to_readable_code(self):
        response = self._handle(InvalidToken())

        self.assert_error(response, 401, "invalid_token", "Invalid Token format")

    def test_permission_denied_uses_stable_403_contract(self):
        response = self._handle(PermissionDenied("Not allowed."))

        self.assert_error(response, 403, "permission_denied", "Not allowed.")

    def test_not_found_uses_stable_404_contract(self):
        response = self._handle(NotFound("Customer not found."))

        self.assert_error(response, 404, "not_found", "Customer not found.")

    def test_duplicate_record_uses_stable_409_contract(self):
        response = self._handle(DuplicatedRecord())

        self.assert_error(
            response,
            409,
            "duplicated_record",
            "Duplicate record does not allow",
        )

    def test_unsupported_media_type_uses_stable_415_contract(self):
        response = self._handle(UnsupportedMediaType("application/xml"))

        self.assert_error(response, 415, "unsupported_media_type")


class CoreErrorMiddlewareTests(SimpleTestCase):
    def test_unhandled_exception_returns_json_500_contract(self):
        request = RequestFactory().get("/api/v1/data/example/")
        middleware = CoreErrorMiddleware(lambda request: None)

        response = middleware.process_exception(request, RuntimeError("database leaked"))
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertTrue(response["Content-Type"].startswith("application/json"))
        self.assertEqual(
            payload,
            {
                "error": {
                    "code": "internal_error",
                    "message": "Internal server error",
                    "fields": {},
                }
            },
        )
        self.assertNotContains(response, "database leaked", status_code=500)
