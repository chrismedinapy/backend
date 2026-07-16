"""JWT issuing and validation helpers for the public authentication contract."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from decouple import config

from data.utils import exceptions

REQUIRED_CLAIMS = (
    "sub",
    "user_code",
    "name",
    "access_level",
    "token_type",
    "iat",
    "exp",
    "jti",
)


def _now():
    return datetime.now(timezone.utc)


def _encode(user, token_type, lifetime_seconds, now=None):
    issued_at = now or _now()
    expires_at = issued_at + timedelta(seconds=lifetime_seconds)
    user_code = str(user.user_login_code)
    payload = {
        "sub": user_code,
        "user_code": user_code,
        "name": user.name,
        "access_level": user.status,
        "token_type": token_type,
        "iat": issued_at,
        "exp": expires_at,
        "jti": str(uuid4()),
    }
    token = jwt.encode(
        payload,
        config("SECRET_KEY"),
        algorithm=config("ALGORITHM"),
    )
    return token, int(lifetime_seconds)


def issue_token_pair(user, now=None):
    access_seconds = config("ACCESS_TOKEN_EXPIRE_SECONDS", default=86400, cast=int)
    refresh_seconds = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7, cast=int) * 86400
    access_token, expires_in = _encode(user, "access", access_seconds, now=now)
    refresh_token, _ = _encode(user, "refresh", refresh_seconds, now=now)
    user_code = str(user.user_login_code)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "user": {
            "user_code": user_code,
            "name": user.name,
            "access_level": user.status,
        },
        # Temporary aliases for existing clients. New consumers must use the
        # access_token and nested user fields above.
        "token": access_token,
        "user_code": user_code,
        "name": user.name,
    }


def decode_token(token, expected_type):
    try:
        payload = jwt.decode(
            token,
            config("SECRET_KEY"),
            algorithms=[config("ALGORITHM")],
            options={"require": list(REQUIRED_CLAIMS)},
        )
    except jwt.ExpiredSignatureError as exc:
        raise exceptions.ExpiredToken() from exc
    except jwt.MissingRequiredClaimError as exc:
        raise exceptions.InvalidToken("Token is missing required claims") from exc
    except jwt.InvalidTokenError as exc:
        raise exceptions.InvalidToken() from exc

    if payload.get("token_type") != expected_type:
        raise exceptions.InvalidToken(f"Expected a {expected_type} token")
    if payload.get("sub") != payload.get("user_code"):
        raise exceptions.InvalidToken("Token subject does not match user_code")
    return payload
