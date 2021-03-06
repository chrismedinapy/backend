from rest_framework import serializers
from data.utils.validator import MyUsernameValidator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=4, max_length=50, validators=[MyUsernameValidator()])
    password = serializers.CharField(min_length=6)


class LoginRefreshSerializer(serializers.Serializer):
    user_code = serializers.UUIDField()
    old_token = serializers.CharField(min_length=25)
