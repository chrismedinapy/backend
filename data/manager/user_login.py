from django.db import models, IntegrityError
from data.utils.constant import Status
from data.utils.exceptions import EntityNotFound, DuplicatedRecord, InvalidOperation


class UserLoginQuerySet(models.QuerySet):
    def authenticate(self, username, password):
        return self.get(username=username, password=password, status=Status.ACTIVE.value)

    def get_all(self):
        return self.filter(status=Status.ACTIVE.value).values('user_login_code', 'username', 'name', 'email')

    def get_by_code(self, code):
        return self.filter(user_login_code=code, status=Status.ACTIVE.value).first()

    def get_by_username(self, username):
        return self.filter(status=Status.ACTIVE.value, username=username).first()


class UserLoginManager(models.Manager):
    def get_queryset(self):
        return UserLoginQuerySet(self.model, using=self._db)

    def authenticate(self, username, password):
        try:
            return self.get_queryset().authenticate(username, password)
        except models.ObjectDoesNotExist:
            raise EntityNotFound('User was not found')

    def get_all_users(self):
        return self.get_queryset().get_all()

    def get_user_by_code(self, code):
        return self.get_queryset().get_by_code(code)

    def get_user_by_name(self, user_name):
        return self.get_queryset().get_by_username(user_name)

    def save(self, user_login):
        try:
            user_login.save()
            return user_login
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save user \n Error Message:{ex}")
