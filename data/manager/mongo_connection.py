import base64
import json
from importlib import import_module
import uuid
import gridfs
from simplejson import dumps
from data.utils.mongo_client import get_client, get_gridf_db
from data.utils.exceptions import EntityNotFound, InvalidOperation
from data.models.customer_input import CustomerInput
from bson.objectid import ObjectId


class MongoCollection:
    def __init__(self):
        self.db = get_client()

    def get_collection(self, name="customer_products"):
        return self.db[name]

    def save_customer_product(self, customer_code, customer_data):
        try:
            collection = self.get_collection("customer_products")
            condition_filter = {
                "customer_code": customer_code
            }
            collection.update_one(
                condition_filter, {"$set": customer_data}, upsert=True)
        except Exception as ex:
            raise EntityNotFound(
                f"No customer with code: {customer_code} has been found, message: {ex}"
            )

    def save_customer_with_gridfs(self, customer_data, customer_input_code):
        get_conn = get_client()
        try:
            fs = gridfs.GridFS(get_conn)
            gridfs_code = fs.put(customer_data, encoding='utf-8')
            print(f" File uploaded, name:, code: {gridfs_code}")
            customer_input = CustomerInput.objects.get_customer_input_by_code(
                customer_input_code)
            customer_input.gridfs_code = gridfs_code
            CustomerInput.objects.save(customer_input)
        except Exception as ex:
            raise InvalidOperation(
                f"Error saving with gridf, message: {ex}"
            )

    def list_customer_input_with_gridfs(self, customer_code, gridfs_code):
        get_conn = get_client()

        try:
            customer_input = CustomerInput.objects.get_customer_input_by_customer_code_and_gridfs_code(
                customer_code, gridfs_code)
            if customer_input:
                fs = gridfs.GridFS(get_conn)
                object_id = ObjectId(gridfs_code)
                customer_input_gridfs = fs.get(object_id).read()
                customer_input_json = json.loads(customer_input_gridfs)
                return customer_input_json
            else:
                raise EntityNotFound(
                    f"There is no customer with customer_code: {customer_code}"
                )
        except Exception as ex:
            raise InvalidOperation(
                f"Error trying to list gridfs, message: {ex}"
            )

    def get_customer_product(self, customer_code):
        collection = self.get_collection("customer_products")
        return list(collection.find({"customer_code": customer_code}))
