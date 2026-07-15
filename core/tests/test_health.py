from django.test import SimpleTestCase
from django.urls import reverse


class HealthcheckTests(SimpleTestCase):
    expected_payload = {
        "status": "ok",
        "service": "datacore-api",
    }

    def test_root_healthcheck_returns_stable_json(self):
        response = self.client.get(reverse("healthcheck"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json(), self.expected_payload)

    def test_versioned_healthcheck_returns_stable_json(self):
        response = self.client.get(reverse("api-v1-healthcheck"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json(), self.expected_payload)

    def test_healthchecks_reject_non_get_requests(self):
        for route_name in ("healthcheck", "api-v1-healthcheck"):
            with self.subTest(route_name=route_name):
                response = self.client.post(reverse(route_name))
                self.assertEqual(response.status_code, 405)
