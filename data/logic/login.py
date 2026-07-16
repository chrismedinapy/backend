from data.models.user import User
from data.security.tokens import decode_token, issue_token_pair
from data.utils.encryptor import Encryptor
from data.utils.exceptions import InvalidToken


def authenticate(login_payload):
    username = login_payload.get("username").lower()
    password = login_payload.get("password")
    password_encrypted = Encryptor.md5_encryption(password)

    user = User.objects.authenticate(username, password_encrypted)
    return issue_token_pair(user)


def refresh_token(payload):
    refresh_token_value = payload.get("refresh_token") or payload.get("old_token")
    token_payload = decode_token(refresh_token_value, expected_type="refresh")

    legacy_user_code = payload.get("user_code")
    if legacy_user_code and str(legacy_user_code) != token_payload["user_code"]:
        raise InvalidToken("Token subject does not match user_code")

    user = User.objects.get_user_by_code(token_payload["user_code"])
    if not user:
        raise InvalidToken("Token user does not exist")
    return issue_token_pair(user)
