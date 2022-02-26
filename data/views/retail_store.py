from data.logic.retail_store import RetailStoreLogic
from rest_framework.viewsets import ViewSet
from data.serializers.retail_store import RetailStoreSerializers

from data.utils.validator import body_validator, uuid_validator

class RetailStoreViewClass(ViewSet):
    retail_store_logic = RetailStoreLogic()

    def create(self, request, customer_code):
        body_validator(request.data, RetailStoreSerializers)
        uuid_validator(customer_code)
        self.customer_store_logic.create(request.data, customer_code)