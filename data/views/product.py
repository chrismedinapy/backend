from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from data.logic.product import ProductLogic
from data.serializers.product import ProductSerializers
from data.utils.validator import body_validator, uuid_validator


class ProductViewClass(ViewSet):
    product_logic = ProductLogic()

    def create(self, request):
        body_validator(request.data, ProductSerializers)
        self.product_logic.create(request.data)

        return Response(status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get_products(self, request):
        product_list = self.product_logic.get_products()
        return Response(product_list, status=status.HTTP_200_OK)

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def get_product(self, request, product_code):
        uuid_validator(product_code)
        product = self.product_logic.get_product_by_code(product_code)
        return Response(product, status=status.HTTP_200_OK)

    def delete(self, resquest, product_code):
        uuid_validator(product_code)
        product = self.product_logic.delete(product_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, product_code):
        uuid_validator(product_code)
        print(request.data)
        body_validator(request.data, ProductSerializers)
        product = self.product_logic.update(product_code, request.data)
        return Response(product, status=status.HTTP_200_OK)
