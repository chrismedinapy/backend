

import uuid

from django.contrib.gis.geos import Point
from data.models.retail_store import RetailStore, Customer
from data.utils.constant import Status
from data.utils.exceptions import EntityNotFound, InvalidParameter


class RetailStoreLogic():
    def __init__(self) -> None:
        self.fields = ["retail_store_code", "retail_store_name",
                       "retail_store_location", "retail_store_city"]

    def create(self, retail_store_data, customer_code):
        retail_store_code = str(uuid.uuid4())
        retail_store_name = retail_store_data.get("retail_store_name")
        retail_store_location = retail_store_data.get("retail_store_location")
        if not retail_store_location["latitude"] or not retail_store_location["longitude"]:
            raise InvalidParameter(
                f"Missing longitude or latitude fields."
            )
        point = Point(retail_store_location["latitude"], retail_store_location["longitude"])
        retail_store_city = retail_store_data.get("retail_store_city")
        retail_store_status = Status.ACTIVE.value

        customer = Customer.objects.get_customer_by_code(customer_code)
        if not customer:
            raise EntityNotFound(
                f"Customer with code: {customer_code} not found"
            )
        new_retail_store = RetailStore(retail_store_code=retail_store_code,
                                       retail_store_name=retail_store_name,
                                       retail_store_location=point,
                                       retail_store_city = retail_store_city,
                                       status=retail_store_status,
                                       customer=customer)
        new_retail_saved = RetailStore.objects.save(new_retail_store)
