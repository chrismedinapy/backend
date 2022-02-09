from rest_framework.test import APITestCase
from rest_framework import status

from data.logic.user import UserLogic
from data.tests.helper.authorization_helper import http_authorization_setup_by_current_user
from data.tests.mock.user_login import new_user_mock
from data.tests.mock.customer import customer_mock
from data.tests.seeders.seed_user import seed_user


class CreateCustomerTestCase(APITestCase):
    def setUp(self):
     # seed a super staff
        self.user_logic = UserLogic()
        self.user_logic.create(new_user_mock)
        username = new_user_mock.get('username')
        password = new_user_mock.get('password')

        # set token to http authorization header
        self.current_user_code = http_authorization_setup_by_current_user(
            username, password, self.client)

        # set urlt
        self.url = '/data/customers/'

    def test_can_create_customer(self):
        customer_payload = customer_mock
        response = self.client.post(self.url, customer_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
