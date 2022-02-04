from urllib import response
from rest_framework import status
from rest_framework.test import APITestCase
from data.logic.user import UserLogic
from data.tests.mock.user_login import new_user_mock


class CreateUserTestCase(APITestCase):

    def setUp(self):
        # seed a super staff
        self.user_signup_logic = UserLogic()

        # set the default end point
        self.url = f'/data/users/signup/'

    def test_create_user(self):
        new_user = new_user_mock
        response = self.client.post(
            self.url, new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_wrong_email(self):
        new_user_wrong_email = new_user_mock.copy()
        new_user_wrong_email["email"] = "work.email"
        response = self.client.post(
            self.url, new_user_wrong_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_weak_password(self):
        new_user_weak_password = new_user_mock.copy()
        new_user_weak_password["password"] = 'weakpassword'
        response = self.client.post(
            self.url, new_user_weak_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_wrong_number(self):
        new_user_wrong_number = new_user_mock.copy()
        new_user_wrong_number["phone_number"] = 'bad_phone_number'
        response = self.client.post(
            self.url, new_user_wrong_number, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
