"""Regression tests for the production runtime boundary."""

import importlib.util
import json
import logging
import os
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from core.logging import JsonFormatter, RequestIdFilter
from middleware.request_id import RequestIdMiddleware, request_id_context


class ProductionRuntimeTests(SimpleTestCase):
    def test_request_id_is_preserved_and_returned(self):
        request = RequestFactory().get("/api/v1/health/", HTTP_X_REQUEST_ID="frontend-123")
        response = RequestIdMiddleware(lambda received: HttpResponse(received.request_id))(request)

        self.assertEqual(response.content.decode(), "frontend-123")
        self.assertEqual(response["X-Request-ID"], "frontend-123")

    def test_invalid_request_id_is_replaced(self):
        request = RequestFactory().get("/api/v1/health/", HTTP_X_REQUEST_ID="invalid value")
        response = RequestIdMiddleware(lambda received: HttpResponse(received.request_id))(request)

        generated = response["X-Request-ID"]
        self.assertNotEqual(generated, "invalid value")
        self.assertEqual(len(generated), 32)

    def test_json_logging_contains_request_id(self):
        token = request_id_context.set("request-456")
        try:
            record = logging.LogRecord("runtime", logging.INFO, __file__, 1, "ready", (), None)
            RequestIdFilter().filter(record)
            payload = json.loads(JsonFormatter().format(record))
        finally:
            request_id_context.reset(token)

        self.assertEqual(payload["message"], "ready")
        self.assertEqual(payload["request_id"], "request-456")
        self.assertEqual(payload["level"], "INFO")

    def test_gunicorn_environment_is_validated(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "gunicorn.conf.py")
        spec = importlib.util.spec_from_file_location("gunicorn_config_test", path)
        module = importlib.util.module_from_spec(spec)

        with patch.dict(os.environ, {"PORT": "9000", "GUNICORN_WORKERS": "3"}, clear=False):
            spec.loader.exec_module(module)

        self.assertEqual(module.bind, "0.0.0.0:9000")
        self.assertEqual(module.workers, 3)
        self.assertEqual(module.accesslog, "-")
        self.assertEqual(module.errorlog, "-")

    def test_gunicorn_rejects_non_positive_values(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "gunicorn.conf.py")
        spec = importlib.util.spec_from_file_location("gunicorn_config_invalid_test", path)
        module = importlib.util.module_from_spec(spec)

        with patch.dict(os.environ, {"GUNICORN_WORKERS": "0"}, clear=False):
            with self.assertRaises(ValueError):
                spec.loader.exec_module(module)
