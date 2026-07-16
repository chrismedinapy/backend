from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from data.logic import login
from data.serializers.login import LoginRefreshSerializer, LoginSerializer
from data.utils.validator import body_validator


class LoginViewSet(ViewSet):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    login_logic = login

    def authenticate(self, request):
        payload = body_validator(request.data, LoginSerializer)
        return Response(self.login_logic.authenticate(payload))

    def refresh_token(self, request):
        payload = body_validator(request.data, LoginRefreshSerializer)
        return Response(self.login_logic.refresh_token(payload))
