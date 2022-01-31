from data import models
from data.utils.constant import AccessLevel, Status
from data.utils.encryptor import Encryptor


class UserLoginLogic():

    def __init__(self):
        self.field = ['name', 'email', 'phone_number']

    def create(self, user_login_data):

        username = user_login_data.get('username').lower()
        email = user_login_data.get('email').lower()
        password = user_login_data.get('password')
        password_encrypted = Encryptor.md5_encryption(password)
        name = user_login_data.get('name')
        phone_number = user_login_data.get('phone_number')
        new_user_login = models.UserLogin(username=username,
                                          name=name,
                                          password=password_encrypted,
                                          email=email,
                                          phone_number=phone_number,
                                          status=Status.ACTIVE.value
                                          )
        user_login_saved = models.UserLogin.objects.save(new_user_login)

        return user_login_data
