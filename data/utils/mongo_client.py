from pymongo import MongoClient
from decouple import config

def get_client(db_name=config("MONGO_INITDB_DATABASE")):
        mongo_conn=MongoClient(
            host=['mongodb:27017'], document_class=dict, tz_aware=False, connect=True)
        return mongo_conn[db_name]

#class MongoConnection(object):

    # def get_client(db_name=config("MONGO_INITDB_DATABASE")):
    #     mongo_conn=MongoClient(
    #         host=['mongodb:27017'], document_class=dict, tz_aware=False, connect=True)
    #     return mongo_conn[db_name]

#    def __init__(self):
#        host = config("MONGO_HOST")
#        port = config("MONGO_PORT")
#        client = MongoClient(host=['mongodb:27017'], document_class=dict, tz_aware=False, connect=True)
#        self.db = client[config("MONGO_INITDB_DATABASE")]
#
#    def get_collection(self, name):
#        self.collection = self.db[name]
#
