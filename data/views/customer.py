from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from data.logic.customer import CustomerLogic
from data.serializers.customer import CustomerSerializers
from data.utils.validator import body_validator, uuid_validator


class CustomerViewClass(ViewSet):
    customer_logic = CustomerLogic()

    def create(self, request):
        body_validator(request.data, CustomerSerializers)
        self.customer_logic.create(request.data)

        return Response(status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get_customers(self, request):
        customer_list = self.customer_logic.get_customers()
        return Response(customer_list, status=status.HTTP_200_OK)

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get_customer(self, request, customer_code):
        uuid_validator(customer_code)
        customer = self.customer_logic.get_customer_by_code(customer_code)
        return Response(customer, status=status.HTTP_200_OK)

    def delete(self, resquest, customer_code):
        uuid_validator(customer_code)
        customer = self.customer_logic.delete(customer_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, customer_code):
        uuid_validator(customer_code)
        print(request.data)
        body_validator(request.data, CustomerSerializers)
        customer = self.customer_logic.update(customer_code, request.data)
        return Response(customer, status=status.HTTP_200_OK)