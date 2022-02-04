import jwt
import datetime
from decouple import config
from data.models.user import User
from data.utils.encryptor import Encryptor
from data.utils.exceptions import ExpiredToken


def authenticate(login_payload):
    username = login_payload.get('username').lower()
    password = login_payload.get('password')
    password_encrypted = Encryptor.md5_encryption(password)

    try:
        user_login = User.objects.authenticate(
            username, password_encrypted)
        user_login_code = str(user_login.user_login_code)
        name = user_login.name
        status = user_login.status

        token = __generate_jwt_token(user_login_code, name, status)

        return {
            "token": token,
            "user_code": user_login_code,
            "name": name,
        }
    except Exception as error:
        raise error


def refresh_token(payload):
    token = payload.get("old_token")
    user_code = payload.get("user_code")
    try:
        old_token_payload = jwt.decode(
            token, config("SECRET_KEY"), algorithms=config("ALGORITHM")
        )
        if old_token_payload.get("user_code") == user_code:
            old_token_values = old_token_payload.values()
            refresh_token = __generate_jwt_token(*old_token_payload)
            return {
                "token": refresh_token
            }
        raise Exception('Invalid Token')

    except jwt.ExpiredSignatureError:
        raise ExpiredToken("Token expired, please login again.")

def __generate_jwt_token(user_login_code, name, status, now=None, *args, expiration_days=int(config("ACCESS_TOKEN_EXPIRE_DAYS"))):
    if not now:
        now = datetime.datetime.utcnow()
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days)
    token_payload = {
        "user_code": user_login_code,
        "name": name,
        "status": status,
        "iat": now,
        "exp": expiration,
    }
    token = jwt.encode(token_payload, config("SECRET_KEY"),
                       algorithm=config("ALGORITHM"))
    return f"{token}"
