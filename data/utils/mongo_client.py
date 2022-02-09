from pymongo import MongoClient
from decouple import config


def get_client(db_name=config("MONGO_INITDB_DATABASE")):
    host = config("MONGO_HOST")
    port = config("MONGO_PORT")
    mongo_conn = MongoClient(
        host=[f'{host}:{port}'], document_class=dict, tz_aware=False, connect=True)
    return mongo_conn[db_name]
