"""Compatibility tests for the authentication contract migration."""

from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase

from data.logic import login
from data.security.tokens import issue_token_pair
from data.serializers.login import LoginRefreshSerializer
from data.utils.exceptions import InvalidToken


class LoginResponseCompatibilityTests(TestCase):
    @patch("data.security.tokens.config")
    def test_new_response_keeps_legacy_login_aliases(self, config):
        values = {
            "SECRET_KEY": "test-secret",
            "ALGORITHM": "HS256",
            "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,
            "REFRESH_TOKEN_EXPIRE_DAYS": 7,
        }
        config.side_effect = lambda name, default=None, cast=None: (
            cast(values.get(name, default)) if cast else values.get(name, default)
        )
        user = SimpleNamespace(user_login_code=uuid4(), name="User", status=1)

        response = issue_token_pair(user)

        self.assertEqual(response["token"], response["access_token"])
        self.assertEqual(response["user_code"], response["user"]["user_code"])
        self.assertEqual(response["name"], response["user"]["name"])


class RefreshCompatibilityTests(TestCase):
    def test_serializer_accepts_new_and_legacy_refresh_shapes(self):
        new_payload = LoginRefreshSerializer(
            data={"refresh_token": "n" * 25}
        )
        legacy_payload = LoginRefreshSerializer(
            data={"old_token": "o" * 25, "user_code": uuid4()}
        )

        self.assertTrue(new_payload.is_valid(), new_payload.errors)
        self.assertTrue(legacy_payload.is_valid(), legacy_payload.errors)

    @patch("data.logic.login.issue_token_pair")
    @patch("data.logic.login.User.objects.get_user_by_code")
    @patch("data.logic.login.decode_token")
    def test_legacy_refresh_still_derives_identity_from_signed_token(
        self,
        decode,
        get_user,
        issue_pair,
    ):
        user_code = uuid4()
        user = SimpleNamespace(user_login_code=user_code, name="User", status=1)
        decode.return_value = {"user_code": str(user_code)}
        get_user.return_value = user
        issue_pair.return_value = {"access_token": "new", "refresh_token": "new-r"}

        result = login.refresh_token(
            {"old_token": "legacy-refresh", "user_code": user_code}
        )

        decode.assert_called_once_with("legacy-refresh", expected_type="refresh")
        self.assertEqual(result["access_token"], "new")

    @patch("data.logic.login.decode_token")
    def test_legacy_user_code_cannot_override_token_identity(self, decode):
        decode.return_value = {"user_code": str(uuid4())}

        with self.assertRaises(InvalidToken):
            login.refresh_token(
                {"old_token": "legacy-refresh", "user_code": uuid4()}
            )
