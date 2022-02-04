from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from data.logic.user import UserLogic
from data.serializers.user_login import UserAddSerializer
from data.utils.validator import body_validator


class UserView(ViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    user_login_logic = UserLogic()

    def create(self, request):
        body_validator(request.data, UserAddSerializer)
        self.user_login_logic.create(request.data)

        return Response(status=status.HTTP_201_CREATED)
