import base64
import hashlib
import json
from importlib import import_module
import uuid

import gridfs
from bson.objectid import ObjectId
from gridfs.errors import FileExists
from pymongo.errors import DuplicateKeyError
from simplejson import dumps

from data.models.customer_input import CustomerInput
from data.utils.exceptions import EntityNotFound, InvalidOperation
from data.utils.mongo_client import get_client, get_gridf_db


class MongoCollection:
    def __init__(self):
        self.db = get_client()

    def get_collection(self, name="customer_products"):
        return self.db[name]

    def save_customer_product(self, customer_code, customer_data):
        try:
            collection = self.get_collection("customer_products")
            condition_filter = {"customer_code": customer_code}
            collection.update_one(
                condition_filter, {"$set": customer_data}, upsert=True
            )
        except Exception as ex:
            raise EntityNotFound(
                f"No customer with code: {customer_code} has been found, message: {ex}"
            ) from ex

    @staticmethod
    def _gridfs_object_id(customer_input_code):
        """Return a stable GridFS identifier for one CustomerInput record."""

        digest = hashlib.sha256(
            str(customer_input_code).encode("utf-8")
        ).digest()
        return ObjectId(digest[:12])

    def save_customer_with_gridfs(self, customer_data, customer_input_code):
        get_conn = get_client()
        try:
            fs = gridfs.GridFS(get_conn)
            gridfs_code = self._gridfs_object_id(customer_input_code)

            if not fs.exists(gridfs_code):
                try:
                    fs.put(
                        customer_data,
                        _id=gridfs_code,
                        encoding="utf-8",
                        metadata={
                            "customer_input_code": str(customer_input_code)
                        },
                    )
                except (DuplicateKeyError, FileExists):
                    # Another worker completed the same deterministic write first.
                    pass

            customer_input = CustomerInput.objects.get_customer_input_by_code(
                customer_input_code
            )
            customer_input.gridfs_code = str(gridfs_code)
            CustomerInput.objects.save(customer_input)
            print(f"File uploaded or reused, code: {gridfs_code}")
            return gridfs_code
        except Exception as ex:
            raise InvalidOperation(
                f"Error saving with gridf, message: {ex}"
            ) from ex

    def list_customer_input_with_gridfs(self, customer_code, gridfs_code):
        get_conn = get_client()

        try:
            customer_input = CustomerInput.objects.get_customer_input_by_customer_code_and_gridfs_code(
                customer_code, gridfs_code
            )
            if customer_input:
                fs = gridfs.GridFS(get_conn)
                object_id = ObjectId(gridfs_code)
                customer_input_gridfs = fs.get(object_id).read()
                customer_input_json = json.loads(customer_input_gridfs)
                return customer_input_json
            raise EntityNotFound(
                f"There is no customer with customer_code: {customer_code}"
            )
        except Exception as ex:
            raise InvalidOperation(
                f"Error trying to list gridfs, message: {ex}"
            ) from ex

    def get_customer_product(self, customer_code):
        collection = self.get_collection("customer_products")
        return list(collection.find({"customer_code": customer_code}))
