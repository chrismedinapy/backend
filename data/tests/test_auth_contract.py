"""Contract and regression tests for JWT authentication."""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

import jwt
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from data.logic import login
from data.security.tokens import decode_token, issue_token_pair
from data.utils.exceptions import ExpiredToken, InvalidToken
from middleware.security.authentication import CoreAuthentication
from middleware.security.permission import CorePermission

SECRET = "test-secret"
ALGORITHM = "HS256"


def fake_config(name, default=None, cast=None):
    values = {
        "SECRET_KEY": SECRET,
        "ALGORITHM": ALGORITHM,
        "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,
        "REFRESH_TOKEN_EXPIRE_DAYS": 7,
    }
    value = values.get(name, default)
    return cast(value) if cast else value


class JWTContractTests(TestCase):
    def setUp(self):
        self.user = SimpleNamespace(
            user_login_code=uuid4(),
            name="Frontend User",
            status=1,
        )

    @patch("data.security.tokens.config", side_effect=fake_config)
    def test_login_token_pair_has_stable_frontend_contract(self, _config):
        response = issue_token_pair(self.user)

        self.assertEqual(response["token_type"], "Bearer")
        self.assertEqual(response["expires_in"], 3600)
        self.assertEqual(response["user"]["user_code"], str(self.user.user_login_code))
        self.assertIn("access_token", response)
        self.assertIn("refresh_token", response)

    @patch("data.security.tokens.config", side_effect=fake_config)
    def test_issued_access_token_contains_all_required_claims(self, _config):
        pair = issue_token_pair(self.user)

        payload = decode_token(pair["access_token"], expected_type="access")

        self.assertEqual(payload["sub"], str(self.user.user_login_code))
        self.assertEqual(payload["user_code"], str(self.user.user_login_code))
        self.assertEqual(payload["name"], self.user.name)
        self.assertEqual(payload["access_level"], self.user.status)
        self.assertEqual(payload["token_type"], "access")
        for claim in ("iat", "exp", "jti"):
            self.assertIn(claim, payload)

    @patch("data.security.tokens.config", side_effect=fake_config)
    def test_access_and_refresh_tokens_are_not_interchangeable(self, _config):
        pair = issue_token_pair(self.user)

        with self.assertRaises(InvalidToken):
            decode_token(pair["access_token"], expected_type="refresh")
        with self.assertRaises(InvalidToken):
            decode_token(pair["refresh_token"], expected_type="access")

    @patch("data.security.tokens.config", side_effect=fake_config)
    def test_expired_token_is_reported_separately(self, _config):
        expired = jwt.encode(
            {
                "sub": str(self.user.user_login_code),
                "user_code": str(self.user.user_login_code),
                "name": self.user.name,
                "access_level": self.user.status,
                "token_type": "access",
                "iat": datetime.now(timezone.utc) - timedelta(hours=2),
                "exp": datetime.now(timezone.utc) - timedelta(hours=1),
                "jti": str(uuid4()),
            },
            SECRET,
            algorithm=ALGORITHM,
        )

        with self.assertRaises(ExpiredToken):
            decode_token(expired, expected_type="access")

    @patch("data.security.tokens.config", side_effect=fake_config)
    def test_missing_required_claim_is_rejected(self, _config):
        token = jwt.encode(
            {
                "sub": "user",
                "token_type": "access",
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            },
            SECRET,
            algorithm=ALGORITHM,
        )

        with self.assertRaises(InvalidToken):
            decode_token(token, expected_type="access")

    @patch("data.security.tokens.config", side_effect=fake_config)
    def test_subject_must_match_user_code(self, _config):
        token = jwt.encode(
            {
                "sub": "different-user",
                "user_code": str(self.user.user_login_code),
                "name": self.user.name,
                "access_level": self.user.status,
                "token_type": "access",
                "iat": datetime.now(timezone.utc),
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),
                "jti": str(uuid4()),
            },
            SECRET,
            algorithm=ALGORITHM,
        )

        with self.assertRaises(InvalidToken):
            decode_token(token, expected_type="access")


class LoginLogicTests(TestCase):
    @patch("data.logic.login.issue_token_pair")
    @patch("data.logic.login.User.objects.authenticate")
    @patch("data.logic.login.Encryptor.md5_encryption")
    def test_authenticate_normalizes_username_and_issues_pair(
        self,
        encrypt_password,
        authenticate_user,
        issue_pair,
    ):
        user = SimpleNamespace(user_login_code=uuid4(), name="User", status=1)
        encrypt_password.return_value = "encrypted"
        authenticate_user.return_value = user
        issue_pair.return_value = {"access_token": "access", "refresh_token": "refresh"}

        result = login.authenticate({"username": "FRONTEND", "password": "secret"})

        encrypt_password.assert_called_once_with("secret")
        authenticate_user.assert_called_once_with("frontend", "encrypted")
        issue_pair.assert_called_once_with(user)
        self.assertEqual(result["access_token"], "access")


class CoreAuthenticationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.authentication = CoreAuthentication()

    def test_authorization_header_must_use_exact_bearer_shape(self):
        for value in (None, "Token abc", "Bearer", "bearer abc", "Bearer a b"):
            request = self.factory.get("/api/v1/data/", HTTP_AUTHORIZATION=value or "")
            with self.subTest(value=value), self.assertRaises(InvalidToken):
                self.authentication.authenticate(request)

    @patch("middleware.security.authentication.User.objects.get_user_by_code")
    @patch("middleware.security.authentication.decode_token")
    def test_valid_access_token_returns_payload_and_credentials(
        self,
        decode,
        get_user,
    ):
        payload = {"user_code": str(uuid4()), "token_type": "access"}
        decode.return_value = payload
        get_user.return_value = SimpleNamespace(user_login_code=payload["user_code"])
        request = self.factory.get(
            "/api/v1/data/",
            HTTP_AUTHORIZATION="Bearer valid-token",
        )

        authenticated_user, credentials = self.authentication.authenticate(request)

        decode.assert_called_once_with("valid-token", expected_type="access")
        get_user.assert_called_once_with(payload["user_code"])
        self.assertEqual(authenticated_user, payload)
        self.assertEqual(credentials, "valid-token")
        self.assertEqual(self.authentication.authenticate_header(request), "Bearer")

    @patch("middleware.security.authentication.User.objects.get_user_by_code", return_value=None)
    @patch("middleware.security.authentication.decode_token")
    def test_deleted_token_user_returns_invalid_token(self, decode, _get_user):
        decode.return_value = {"user_code": str(uuid4())}
        request = self.factory.get(
            "/api/v1/data/",
            HTTP_AUTHORIZATION="Bearer valid-token",
        )

        with self.assertRaises(InvalidToken):
            self.authentication.authenticate(request)


class CorePermissionTests(TestCase):
    def test_permission_requires_authenticated_user_code(self):
        permission = CorePermission()

        self.assertTrue(
            permission.has_permission(
                SimpleNamespace(user={"user_code": str(uuid4())}),
                view=None,
            )
        )
        self.assertFalse(
            permission.has_permission(SimpleNamespace(user={}), view=None)
        )
        self.assertFalse(
            permission.has_permission(SimpleNamespace(user=None), view=None)
        )


class RefreshContractTests(TestCase):
    @patch("data.logic.login.issue_token_pair")
    @patch("data.logic.login.User.objects.get_user_by_code")
    @patch("data.logic.login.decode_token")
    def test_refresh_issues_a_new_pair_for_existing_user(self, decode, get_user, issue):
        user = SimpleNamespace(user_login_code=uuid4(), name="User", status=1)
        decode.return_value = {"user_code": str(user.user_login_code)}
        get_user.return_value = user
        issue.return_value = {"access_token": "new-access", "refresh_token": "new-refresh"}

        response = login.refresh_token({"refresh_token": "old-refresh"})

        decode.assert_called_once_with("old-refresh", expected_type="refresh")
        self.assertEqual(response["access_token"], "new-access")
        self.assertEqual(response["refresh_token"], "new-refresh")

    @patch("data.logic.login.User.objects.get_user_by_code", return_value=None)
    @patch("data.logic.login.decode_token", return_value={"user_code": "missing"})
    def test_refresh_rejects_deleted_user(self, _decode, _get_user):
        with self.assertRaises(InvalidToken):
            login.refresh_token({"refresh_token": "old-refresh"})
