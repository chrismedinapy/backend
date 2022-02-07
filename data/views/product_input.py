import json
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from data.logic.product_input import ProductInputLogic
from data.serializers.product_input import ProductInputSerializers
from data.utils.exceptions import InvalidParameter
from data.utils.validator import body_validator, csv_validator


class ProductInputViewClass(ViewSet):
    product_input_logic = ProductInputLogic()

    def create(self, request):
        product_payload = request.data.get("product")
        if not product_payload:
            raise InvalidParameter("Product it's required")
        product = json.loads(product_payload)
        body_validator(product, ProductInputSerializers)

        product_csv = request.data.get("product_csv")
        if not product_csv:
            raise InvalidParameter("CSV File it's required")
        csv_validator(product_csv)

        self.product_input_logic.create(product, product_csv)

        return Response(status=status.HTTP_201_CREATED)
