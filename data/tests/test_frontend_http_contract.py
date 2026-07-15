"""HTTP contract tests that exercise the API as a frontend client would."""

import json
from unittest.mock import patch
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from data.logic.user import UserLogic


class FrontendHttpContractTests(APITestCase):
    """Validate stable browser-facing contracts without calling view internals."""

    def setUp(self):
        suffix = uuid4().hex[:10]
        self.username = f"frontend_{suffix}"
        self.password = f"A!{uuid4().hex}a1"
        UserLogic().create(
            {
                "username": self.username,
                "email": f"{self.username}@example.test",
                "password": self.password,
                "name": "Frontend contract user",
                "phone_number": "595000000000",
            }
        )

    def login(self):
        response = self.client.post(
            "/api/v1/data/users/login/",
            {"username": self.username, "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        return response

    def authorize(self, access_token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_login_and_refresh_publish_the_stable_token_contract(self):
        login_response = self.login()
        login_payload = login_response.json()

        self.assertEqual(login_payload["token_type"], "Bearer")
        self.assertGreater(login_payload["expires_in"], 0)
        self.assertEqual(login_payload["user"]["name"], "Frontend contract user")
        self.assertIn("access_token", login_payload)
        self.assertIn("refresh_token", login_payload)

        refresh_response = self.client.post(
            "/api/v1/data/users/login/refresh/",
            {"refresh_token": login_payload["refresh_token"]},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK, refresh_response.data)
        refresh_payload = refresh_response.json()
        self.assertEqual(refresh_payload["token_type"], "Bearer")
        self.assertNotEqual(refresh_payload["access_token"], login_payload["access_token"])
        self.assertNotEqual(refresh_payload["refresh_token"], login_payload["refresh_token"])

    @patch("data.views.customer.CustomerViewClass.customer_logic.get_customers")
    def test_authenticated_collection_exposes_frontend_pagination(self, get_customers):
        get_customers.return_value = [
            {
                "customer_code": str(uuid4()),
                "customer_name": "Beta customer",
                "customer_description": "Second",
            },
            {
                "customer_code": str(uuid4()),
                "customer_name": "Alpha customer",
                "customer_description": "First",
            },
        ]
        access_token = self.login().json()["access_token"]
        self.authorize(access_token)

        response = self.client.get(
            "/api/v1/data/customers/?search=customer&ordering=customer_name&page=1&page_size=1"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        payload = response.json()
        self.assertEqual(set(payload), {"count", "next", "previous", "results"})
        self.assertEqual(payload["count"], 2)
        self.assertIsNone(payload["previous"])
        self.assertIn("page=2", payload["next"])
        self.assertEqual(payload["results"][0]["customer_name"], "Alpha customer")

    def test_missing_token_uses_the_standard_error_envelope(self):
        response = self.client.get("/api/v1/data/customers/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        payload = response.json()
        self.assertEqual(set(payload), {"error"})
        self.assertIn("code", payload["error"])
        self.assertIn("message", payload["error"])

    @patch("data.views.customer.CustomerViewClass.customer_logic.get_customers")
    def test_invalid_frontend_query_uses_the_standard_error_envelope(self, get_customers):
        get_customers.return_value = []
        access_token = self.login().json()["access_token"]
        self.authorize(access_token)

        response = self.client.get("/api/v1/data/customers/?ordering=private_field")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        payload = response.json()
        self.assertEqual(payload["error"]["code"], "invalid_parameter")

    @patch("data.views.customer_input.CustomerInputViewClass.customer_input_logic.create")
    def test_authenticated_multipart_upload_contract(self, create_customer_input):
        access_token = self.login().json()["access_token"]
        self.authorize(access_token)
        customer_code = str(uuid4())
        retail_store_code = str(uuid4())
        csv_file = SimpleUploadedFile(
            "frontend-contract.csv",
            b"product,quantity\ncoffee,2\n",
            content_type="text/csv",
        )

        response = self.client.post(
            (
                f"/api/v1/data/customers/{customer_code}/retail-store/"
                f"{retail_store_code}/products/"
            ),
            {
                "customer": json.dumps(
                    {"customer_input_description": "Frontend multipart contract"}
                ),
                "customer_csv": csv_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        create_customer_input.assert_called_once()
        customer_payload, uploaded_file, called_customer, called_store = (
            create_customer_input.call_args.args
        )
        self.assertEqual(
            customer_payload["customer_input_description"],
            "Frontend multipart contract",
        )
        self.assertEqual(uploaded_file.name, "frontend-contract.csv")
        self.assertEqual(called_customer, customer_code)
        self.assertEqual(called_store, retail_store_code)
