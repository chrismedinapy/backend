import json
from data.utils.paginator import CustomPageNumberPaginator
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from data.logic.customer_input import CustomerInputLogic
from data.serializers.customer_input import CustomerInputSerializers
from data.utils.exceptions import InvalidParameter
from data.utils.validator import body_validator, csv_validator, uuid_validator


class CustomerInputViewClass(ViewSet):
    customer_input_logic = CustomerInputLogic()

    def create(self, request, customer_code, retail_store_code):
        uuid_validator(customer_code)
        uuid_validator(retail_store_code)
        customer_payload = request.data.get("customer")
        if not customer_payload:
            raise InvalidParameter("Field 'customer' it's required")
        customer = json.loads(customer_payload)
        body_validator(customer, CustomerInputSerializers)
        
        customer_csv = request.data.get("customer_csv")
        if not customer_csv:
            raise InvalidParameter("Field 'customer_csv' it's required")
        csv_validator(customer_csv)

        self.customer_input_logic.create(customer, customer_csv, customer_code, retail_store_code)

        return Response(status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, customer_code, retail_store_code):
        pag = CustomPageNumberPaginator()
        uuid_validator(retail_store_code)
        uuid_validator(customer_code)
        customer_input_json = self.customer_input_logic.list(customer_code, retail_store_code)
        results = pag.paginate_queryset(customer_input_json, request)
        return pag.get_paginated_response(results)
