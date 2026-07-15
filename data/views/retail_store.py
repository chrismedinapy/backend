from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from data.api.listing import paginate_list
from data.logic.retail_store import RetailStoreLogic
from data.serializers.retail_store import RetailStoreSerializers
from data.utils.validator import body_validator, uuid_validator


class RetailStoreViewClass(ViewSet):
    retail_store_logic = RetailStoreLogic()

    def create(self, request, customer_code):
        retail_store_data = body_validator(request.data, RetailStoreSerializers)
        uuid_validator(customer_code)
        self.retail_store_logic.create(retail_store_data, customer_code)
        return Response(status=status.HTTP_201_CREATED)

    def get_all(self, request, customer_code):
        uuid_validator(customer_code)
        retail_stores = self.retail_store_logic.get_all(customer_code)
        response = paginate_list(
            request,
            retail_stores,
            search_fields=("retail_store_name", "retail_store_city"),
            ordering_fields=(
                "retail_store_name",
                "retail_store_city",
                "retail_store_code",
            ),
            filter_fields=("retail_store_city",),
            default_ordering="retail_store_name",
        )
        return Response(response, status=status.HTTP_200_OK)

    def get(self, request, customer_code, retail_store_code):
        uuid_validator(customer_code)
        uuid_validator(retail_store_code)
        retail_store = self.retail_store_logic.get(customer_code, retail_store_code)
        return Response(retail_store, status=status.HTTP_200_OK)
