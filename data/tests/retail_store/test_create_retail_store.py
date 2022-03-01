from rest_framework.test import APITestCase
from data.tests.helper.authorization_helper import http_authorization_setup_by_current_user
from data.tests.mock.user_login import new_user_mock
from data.tests.mock.customer import customer_mock
from data.tests.mock.retail_mock import retail_store_mock
from data.logic.customer import CustomerLogic
from rest_framework import status
from data.logic.user import UserLogic
from data.tests.seeders.seed_customer import seed_customer


class CreateRetailStoreTestCase(APITestCase):
    def setUp(self):
        # seed a user
        self.user_logic = UserLogic()
        self.user_logic.create(new_user_mock)
        username = new_user_mock.get('username')
        password = new_user_mock.get('password')

        # set token to thhp authorization header
        self.current_user_code = http_authorization_setup_by_current_user(
            username, password, self.client)

        # seed a customer
        results = seed_customer(customer_mock, self.current_user_code)
        self.customer_code = results["customer_code"]
        # get customer object
        self.url = f'/data/customers/{self.customer_code}/retail-store/'

    def test_can_create_retail_store(self):
        retail_store_payload = retail_store_mock
        response = self.client.post(
            self.url, retail_store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_retail_store_wrong_location(self):
        retail_store_payload = retail_store_mock.copy()
        retail_store_payload["retail_store_location"] = {
            "wrong": "location"
        }
        response = self.client.post(
            self.url, retail_store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_retail_store_without_customer_code(self):
        url = url_without_customer_code = f'/data/customers//retail_store/'
        retail_store_payload = retail_store_mock.copy()
        response = self.client.post(
            url, retail_store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_retail_store_with_unexisting_customer_code(self):
        unexisting_customer_code = 'a0c99f4f-2a7f-4a0c-8301-a1658efbe1b5'
        url = f'/data/customers/{unexisting_customer_code}/retail-store/'
        retail_store_payload = retail_store_mock.copy()
        response = self.client.post(
            url, retail_store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_retail_wrong_customer_code(self):
        bad_customer_code = 'asdfasdf'
        url = f'/data/customers/{bad_customer_code}/retail-store/'
        retail_store_payload = retail_store_mock.copy()
        response = self.client.post(
            url, retail_store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_retail_store_without_name(self):
        retail_store_payload = retail_store_mock.copy()
        retail_store_payload["retail_store_name"] = ""
        response = self.client.post(
            self.url, retail_store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_retail_store_without_city(self):
        retail_store_payload = retail_store_mock.copy()
        retail_store_payload["retail_store_city"] = ""
        response = self.client.post(
            self.url, retail_store_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
