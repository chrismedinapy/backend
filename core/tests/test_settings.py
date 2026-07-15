from django.conf import settings
from django.test import SimpleTestCase

from core.settings import csv_list


class CsvListTests(SimpleTestCase):
    def test_csv_list_strips_whitespace_and_empty_values(self):
        self.assertEqual(
            csv_list(" https://app.example.com, ,http://localhost:3000 "),
            ["https://app.example.com", "http://localhost:3000"],
        )

    def test_csv_list_accepts_an_empty_environment_value(self):
        self.assertEqual(csv_list(""), [])


class FrontendSettingsTests(SimpleTestCase):
    def test_debug_is_a_boolean(self):
        self.assertIsInstance(settings.DEBUG, bool)
        self.assertFalse(settings.DEBUG)

    def test_cors_is_deny_by_default_and_uses_explicit_origins(self):
        self.assertFalse(settings.CORS_ALLOW_ALL_ORIGINS)
        self.assertEqual(
            settings.CORS_ALLOWED_ORIGINS,
            ["http://localhost:3000", "http://127.0.0.1:3000"],
        )

    def test_csrf_trusted_origins_are_loaded_from_environment(self):
        self.assertEqual(
            settings.CSRF_TRUSTED_ORIGINS,
            ["http://localhost:3000"],
        )

    def test_common_middleware_is_registered_once(self):
        common_middleware = "django.middleware.common.CommonMiddleware"
        self.assertEqual(settings.MIDDLEWARE.count(common_middleware), 1)

    def test_cors_middleware_runs_before_common_middleware(self):
        cors_index = settings.MIDDLEWARE.index(
            "corsheaders.middleware.CorsMiddleware"
        )
        common_index = settings.MIDDLEWARE.index(
            "django.middleware.common.CommonMiddleware"
        )
        self.assertLess(cors_index, common_index)
