from data.logic.customer_user_group import CustomerUserGroupLogic
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from data.serializers.customer_user_group import CustomerUserGroupSerialier

from data.utils.validator import body_validator, uuid_validator


class CustomerUserGroupClassView(ViewSet):
    customer_user_group_logic = CustomerUserGroupLogic()

    def create(self, request, customer_code):
        uuid_validator(customer_code)
        body_validator(request.data, CustomerUserGroupSerialier)
        self.customer_user_group_logic.create(
            customer_code, request.user.get('user_code'), request.data)
        return Response(status=status.HTTP_201_CREATED)
