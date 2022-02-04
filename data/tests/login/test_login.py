from rest_framework.test import APITestCase
from rest_framework import status

import json
from data.logic.user import UserLogic
from data.tests.mock.user_login import new_user_mock


class LoginTest(APITestCase):
    def setUp(self):
        self.user_logic = UserLogic()
        self.user_logic.create(new_user_mock)
        self.url = '/data/users/login/'

    def test_user_can_login(self):
        user_payload = {
            "username": new_user_mock.get("username"),
            "password": new_user_mock.get("password")
        }
        response = self.client.post(self.url, data=user_payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_user_return_token(self):
        user_payload = {
            "username": new_user_mock.get("username"),
            "password": new_user_mock.get("password")
        }
        response = self.client.post(self.url, data=user_payload, format='json')
        rb = response.content
        rbtxt = str(rb)
        rbtxt_removed = rbtxt.lstrip(rbtxt[0])
        rbtxt_removed = rbtxt_removed.replace("'","")
        new_dict = json.loads(rbtxt_removed)
        self.assertTrue(new_dict.get("token"))

    def test_login_wrong_password(self):
        user_payload = {
            "username": new_user_mock.get("username"),
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, user_payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_login_wrong_username(self):
        user_payload = {
            "username":"wrongusername",
            "password":new_user_mock.get("password")
        }
        response = self.client.post(self.url, user_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_wrong_get_method(self):
        user_payload = {
            "username": new_user_mock.get("username"),
            "password": new_user_mock.get("password")
        }
        response = self.client.get(self.url, data=user_payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_wrong_put_method(self):
        user_payload = {    
            "username": new_user_mock.get("username"),
            "password": new_user_mock.get("password")
        }
        response = self.client.put(self.url, data=user_payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_wrong_delete_method(self):
        user_payload = {
            "username": new_user_mock.get("username"),
            "password": new_user_mock.get("password")
        }
        response = self.client.delete(self.url, data=user_payload, format='json')
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

