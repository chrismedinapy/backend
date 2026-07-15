from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from data.api.listing import paginate_list
from data.logic.product import ProductLogic
from data.serializers.product import ProductSerializers
from data.utils.validator import body_validator, uuid_validator


class ProductViewClass(ViewSet):
    product_logic = ProductLogic()

    def create(self, request):
        product_data = body_validator(request.data, ProductSerializers)
        self.product_logic.create(product_data)
        return Response(status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get_products(self, request):
        products = self.product_logic.get_products()
        response = paginate_list(
            request,
            products,
            search_fields=("product_name", "product_description"),
            ordering_fields=("product_name", "product_code"),
            default_ordering="product_name",
        )
        return Response(response, status=status.HTTP_200_OK)

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get_product(self, request, product_code):
        uuid_validator(product_code)
        product = self.product_logic.get_product_by_code(product_code)
        return Response(product, status=status.HTTP_200_OK)

    def delete(self, request, product_code):
        uuid_validator(product_code)
        self.product_logic.delete(product_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, product_code):
        uuid_validator(product_code)
        product_data = body_validator(request.data, ProductSerializers)
        product = self.product_logic.update(product_code, product_data)
        return Response(product, status=status.HTTP_200_OK)
