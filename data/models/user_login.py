import uuid
from django.db import models
from data.manager import user_login

from data.models.update_created import UpdatedCreated


class UserLogin(UpdatedCreated):
    user_login_code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=18, unique=True)
    status = models.IntegerField()

    objects = user_login.UserLoginManager()
