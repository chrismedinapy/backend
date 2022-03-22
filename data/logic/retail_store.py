

import uuid
from xml.dom.minidom import Entity

from django.contrib.gis.geos import Point
from django.forms import model_to_dict
from data.models.retail_store import RetailStore, Customer
from data.utils.constant import Status
from data.utils.exceptions import EntityNotFound, InvalidParameter


class RetailStoreLogic():
    def __init__(self) -> None:
        self.fields = ["retail_store_code", "retail_store_name",
                       "retail_store_city"]

    def create(self, retail_store_data, customer_code):
        retail_store_code = str(uuid.uuid4())
        retail_store_name = retail_store_data.get("retail_store_name")
        retail_store_location = retail_store_data.get("retail_store_location")
        if not retail_store_location["latitude"] or not retail_store_location["longitude"]:
            raise InvalidParameter(
                f"Missing longitude or latitude fields."
            )
        point = Point(
            retail_store_location["latitude"], retail_store_location["longitude"])
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
                                       retail_store_city=retail_store_city,
                                       status=retail_store_status,
                                       customer=customer)
        new_retail_saved = RetailStore.objects.save(new_retail_store)

    def get_all(self, customer_code):
        retail_stores = RetailStore.objects.get_all_by_customer_code(
            customer_code)
        if not retail_stores:
            raise EntityNotFound(
                f'There are no Retail store.'
            )
        retail_store_list = []
        for retail in retail_stores:
            retail_store_list.append(self.__retail_store_mapped(retail))
        return retail_store_list

    def get(self, customer_code, retail_store_code):
        customer = Customer.objects.get_customer_by_code(customer_code)
        if not customer:
            raise EntityNotFound(
                f"Customer with code: {customer_code} not found")

        retail_store = RetailStore.objects.get_retail_store_by_code(
            retail_store_code)
        if not retail_store:
            raise EntityNotFound(
                f"Retail store with code: {retail_store_code} not found")

        return self.__retail_store_mapped(retail_store)

    def __retail_store_mapped(self, retail_store):
        retail_store_dict = model_to_dict(retail_store, fields=self.fields)
        point = retail_store.retail_store_location
        retail_store_dict["retail_store_code"] = str(
            retail_store.retail_store_code)
        retail_store_dict["retail_store_location"] = {
            "latitude": point.coords[0],
            "longitude": point.coords[1]
        }
        return retail_store_dict
