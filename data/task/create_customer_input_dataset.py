import numpy as np
import pandas as pd
from celery import shared_task
from django.db.utils import OperationalError
from pymongo.errors import (
    AutoReconnect,
    ConnectionFailure,
    NetworkTimeout,
    ServerSelectionTimeoutError,
)

from data.manager.mongo_connection import MongoCollection


RETRYABLE_EXCEPTIONS = (
    AutoReconnect,
    ConnectionFailure,
    NetworkTimeout,
    OperationalError,
    ServerSelectionTimeoutError,
)


class CustomerInputDataset:
    def __init__(self) -> None:
        self.collection = "customer_product"

    def create_collection(self, csv_file, customer_code):
        df = pd.read_csv(csv_file, sep=',"', engine="python")
        df = df.replace('"', "", regex=True)
        df.columns = df.columns.str.replace('"', "")
        df.columns = df.columns.str.replace(" ", "")
        df.replace("", np.nan)
        columns = df.columns
        rows = df[[columns[0]]].index
        for column in columns:
            for row in range(len(rows)):
                data = df.loc[row, column]
                if data == "":
                    df.loc[row, column] = 0
        return df.to_json(orient="split")


def _is_retryable(exception):
    """Return whether an exception chain contains a transient dependency error."""

    current = exception
    visited = set()
    while current is not None and id(current) not in visited:
        visited.add(id(current))
        if isinstance(current, RETRYABLE_EXCEPTIONS):
            return True
        current = current.__cause__ or current.__context__
    return False


@shared_task(
    bind=True,
    acks_late=True,
    reject_on_worker_lost=True,
    max_retries=3,
)
def create_collection(self, customer_input_code, customer_code, url):
    """Parse and persist one uploaded dataset with bounded transient retries."""

    try:
        customer_input_database = CustomerInputDataset()
        customer_input_json = customer_input_database.create_collection(
            url, customer_input_code
        )
        collection = MongoCollection()
        gridfs_code = collection.save_customer_with_gridfs(
            str(customer_input_json), customer_input_code
        )
        return str(gridfs_code)
    except Exception as exc:
        if not _is_retryable(exc):
            raise

        countdown = min(2 ** self.request.retries, 30)
        raise self.retry(exc=exc, countdown=countdown) from exc
