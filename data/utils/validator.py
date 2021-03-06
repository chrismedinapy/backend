import re
import uuid
from data.utils.constant import AccessLevel
from data.utils.exceptions import FileNotSupported, InvalidParameter
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


def password_validator(password):
    if not password:
        raise InvalidParameter('password is required.')
    elif len(password) < 6:
        raise InvalidParameter(
            "invalid password: password must contain at least 6 characters.")
    else:
        regEx = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]"
        pattern = re.compile(regEx)
        match = re.search(pattern, password)
        if not match:
            raise InvalidParameter(
                "invalid password: password must contain at least 1 uppercase, 1 lowercase, 1 number and 1 special character.")
    return password


def access_level_validator(access_level):
    if access_level:
        try:
            return AccessLevel(access_level).value
        except Exception:
            raise InvalidParameter(
                "access_level is invalid.")
    return access_level


def body_validator(data, serializer):
    body_serialized = serializer(data=data)
    if not body_serialized.is_valid():
        message = body_serialized.errors
        raise InvalidParameter(message)
    return body_serialized.data

def uuid_validator(value):
    try:
        uuid.UUID(value)
    except ValueError:
        raise InvalidParameter(
            "uuid is invalid.")

def csv_validator(file):
    try:
        if not file:
            raise InvalidParameter("File is required.")
        elif file.content_type not in ['text/csv' ]:
            raise FileNotSupported(f"File: {file.name} format is not supported.")
    except:
        raise FileNotSupported(f"Format is not supported.")

@deconstructible
class MyUsernameValidator(validators.RegexValidator):
    """
    Validator for usernames.

    - Only ASCII lowercase letters, numbers and underscore are supported.
    - Must start with a letter.
    """
    regex = r'^[a-z][a-z0-9_]+$'
    message = _(
        'Enter a valid username. This value may contain only lowercase ASCII letters, '
        'numbers, and underscores. Must start with a letter.'
    )
    flags = 0