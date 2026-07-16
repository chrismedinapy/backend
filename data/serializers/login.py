from rest_framework import serializers

from data.utils.validator import MyUsernameValidator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=4,
        max_length=50,
        validators=[MyUsernameValidator()],
    )
    password = serializers.CharField(min_length=6, write_only=True)


class LoginRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        min_length=25,
        trim_whitespace=True,
        required=False,
    )
    old_token = serializers.CharField(
        min_length=25,
        trim_whitespace=True,
        required=False,
        write_only=True,
    )
    user_code = serializers.UUIDField(required=False, write_only=True)

    def validate(self, attrs):
        if not attrs.get("refresh_token") and not attrs.get("old_token"):
            raise serializers.ValidationError(
                {"refresh_token": "A refresh token is required."}
            )
        return attrs
