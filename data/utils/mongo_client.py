from pymongo import MongoClient
from decouple import config
import gridfs


def get_client(db_name=config("MONGO_INITDB_DATABASE")):
    host = config("MONGO_HOST")
    port = config("MONGO_PORT")
    mongo_conn = MongoClient(
        host=['mongodb:27017'], document_class=dict, tz_aware=False, connect=True)
    return mongo_conn[db_name]
def get_gridf_db():
    try:
        conn = MongoClient(host=['mongodb:27017'], document_class=dict, tz_aware=False, connect=True)
        return conn.grid_file
    except Exception as ex:
        print("ERROR, ", ex)