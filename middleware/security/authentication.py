from decouple import config
from rest_framework.authentication import BaseAuthentication

from data.models.user import User
from data.security.tokens import decode_token
from data.utils import exceptions


class CoreAuthentication(BaseAuthentication):
    """Authenticate a strict HTTP Bearer access token."""

    keyword = "Bearer"

    def authenticate(self, request):
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            raise exceptions.InvalidToken("Authorization header is required")

        parts = authorization_header.split()
        if len(parts) != 2 or parts[0] != self.keyword or not parts[1]:
            raise exceptions.InvalidToken(
                "Authorization header must use: Bearer <access_token>"
            )

        payload = decode_token(parts[1], expected_type="access")
        user = User.objects.get_user_by_code(payload["user_code"])
        if not user:
            raise exceptions.InvalidToken("Token user does not exist")

        return payload, parts[1]

    def authenticate_header(self, request):
        return self.keyword
