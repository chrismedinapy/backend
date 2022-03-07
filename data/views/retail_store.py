from data.logic.retail_store import RetailStoreLogic
from rest_framework.viewsets import ViewSet
from data.serializers.retail_store import RetailStoreSerializers
from rest_framework.response import Response
from rest_framework import status
from data.utils.validator import body_validator, uuid_validator


class RetailStoreViewClass(ViewSet):
    retail_store_logic = RetailStoreLogic()

    def create(self, request, customer_code):
        body_validator(request.data, RetailStoreSerializers)
        uuid_validator(customer_code)
        self.retail_store_logic.create(request.data, customer_code)
        return Response(status=status.HTTP_201_CREATED)

    def get_all(self, request, customer_code):
        uuid_validator(customer_code)
        return Response(self.retail_store_logic.get_all(customer_code), status=status.HTTP_200_OK)
