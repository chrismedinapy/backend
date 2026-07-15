from decouple import config
from pymongo import MongoClient


def _create_client():
    """Create a Mongo client from the configured deployment coordinates."""
    return MongoClient(
        host=config("MONGO_HOST"),
        port=config("MONGO_PORT", cast=int),
        document_class=dict,
        tz_aware=False,
        connect=True,
    )


def get_client(db_name=None):
    """Return the configured application database."""
    database_name = db_name or config("MONGO_INITDB_DATABASE")
    return _create_client()[database_name]


def get_gridf_db():
    """Return the configured application database for GridFS operations."""
    return get_client()
