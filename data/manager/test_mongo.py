import uuid
# from data.utils.mongo_client import MongoConnection
from data.utils.mongo_client import get_client
from data.utils.exceptions import EntityNotFound


class TestCollection:
    # class TestCollection(MongoConnection):
    def __init__(self):
        self.db = get_client()
       #super(TestCollection, self).__init__()
       # self.get_collection('Prueba')

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

    def get_customer_product(self, customer_code):
        collection = self.get_collection("customer_products")
        return list(collection.find({"customer_code": customer_code}))

    # def update_and_save(self, obj, json_object):
    #    print("$"*50)
    #    print(obj.customer_input_code)
    #    if self.collection.find({'customer_input_code': obj.customer_input_code}):
    #        self.collection.update_one({ "customer_input_code": obj.customer_input_code},json_object)
    #    else:
    #        self.collection.insert_one({'customer_input_code':obj.customer_input_code},json_object)
    #    #self.collection.insert_one({'customer_input_code':str(uuid.uuid4()),'customer_input_description':'test random'})
    # def remove(self, obj):
    #   if self.collection.find({'customer_input_code': obj.customer_input_code}):
    #        self.collection.delete_one({ "customer_input_code": obj.customer_input_code})
