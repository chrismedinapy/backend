from rest_framework import serializers
from data.utils.validator import MyUsernameValidator


class CustomerUserGroupSerialier(serializers.Serializer):
    username = serializers.CharField(
        max_length=100, validators=[MyUsernameValidator()])
