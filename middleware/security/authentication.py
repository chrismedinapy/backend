import jwt
from rest_framework.authentication import BaseAuthentication

from data.utils import exceptions
from decouple import config


class CoreAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or 'Bearer' not in authorization_header:
            raise exceptions.InvalidToken()

        try:
            access_token = authorization_header.replace('Bearer ', '')
            payload = jwt.decode(
                access_token, config("SECRET_KEY"), algorithms=config("ALGORITHM"))
            return (payload, None)
        except jwt.ExpiredSignatureError:
            raise exceptions.ExpiredToken()
        except (jwt.InvalidSignatureError, jwt.DecodeError):
            raise exceptions.InvalidToken()
