import jwt
from decouple import config
from data import models
from data.serializers.user_login import UserUuidSerializer
from data.utils.constant import AccessLevel, Status
from data.utils.encryptor import Encryptor
from data.utils.exceptions import EntityNotFound, UnauthorizedEntity
from data.utils.validator import body_validator, uuid_validator


class UserLogic():

    def __init__(self):
        self.field = ['user_code', 'name', 'email', 'phone_number']

    def create(self, user_login_data):

        username = user_login_data.get('username').lower()
        email = user_login_data.get('email').lower()
        password = user_login_data.get('password')
        password_encrypted = Encryptor.md5_encryption(password)
        name = user_login_data.get('name')
        phone_number = user_login_data.get('phone_number')
        new_user_mock = models.User(username=username,
                                    name=name,
                                    password=password_encrypted,
                                    email=email,
                                    phone_number=phone_number,
                                    status=Status.ACTIVE.value
                                    )
        user_login_saved = models.User.objects.save(new_user_mock)

        return user_login_data

    def get_by_user_code(self, user_code):
        uuid_validator(user_code)
        user = models.User.objects.get_user_by_code(user_code)
        if not user:
            raise EntityNotFound(
                f"User with code: {user_code} not found"
            )
        return user

    def update(self, user_code, user_data, user_token):
        user = models.User.objects.get_user_by_code(user_code)
        if self.__verify_ownership(user_code, user_token):
            user.username = user_data.get("username")
            user.name = user_data.get("name")
            user.phone_number = user_data.get("phone_number")
            user.email = user_data.get("email")
            password = user_data.get("password")
            encrypted_password = Encryptor.md5_encryption(password)
            user.password = encrypted_password
            updated_user = models.User.objects.save(user)
            return updated_user

    def __verify_ownership(self, user_code, token):
        uuid_validator(user_code)
        token_payload = jwt.decode(
            token, config("SECRET_KEY"), algorithms=config("ALGORITHM"))
        if token_payload.get("user_code") == user_code:
            return True
        else:
            raise UnauthorizedEntity(
                f"You do not have the privilege to update this user "
            )
