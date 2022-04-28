from rest_framework.test import APITestCase
from rest_framework import status
from data.logic.user import UserLogic
from data.tests.helper.authorization_helper import http_authorization_setup_by_current_user
)
from data.tests.mock.user_login import new_user_mock, another_user_mock
from data.tests.mock.customer import customer_mock
from data.tests.seeders.seed_customer import seed_customer


class CreateCustomerTestCase(APITestCase):

    def setUp(self):
        self.user_logic = UserLogic()
        self.user_logic.create(new_user_mock)
        self.user_logic.create(another_user_mock)
        username = new_user_mock.get("username")
        password = new_user_mock.get("password")

        # set token to http authorization header
        self.current_user_code = http_authorization_setup_by_current_user(
            username, password, self.client
        )
        # seed a customer
        results = seed_customer(customer_mock, self.current_user_code)
        self.customer_code = results["customer_code"]
        self.url = f"/data/customers/{self.customer_code}/group/"

    def test_add_new_member(self):
        username = another_user_mock.get("username")
        new_member = {"username": username}
        response = self.client.post(self.url, new_member, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
