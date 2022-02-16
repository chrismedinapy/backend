import json
import io
from data.manager.test_mongo import TestCollection
from celery import shared_task
import pandas as pd
import numpy as np


class CustomerInputDataset():
    def __init__(self) -> None:
        self.collection = 'customer_product'

    def create_collection(self, csv_file, customer_code):
        df = pd.read_csv(csv_file, sep=',"', engine='python')
        df = df.replace('"', "", regex=True)
        df.columns = df.columns.str.replace('"', "")
        df.columns = df.columns.str.replace(' ', "")
        df.replace('', np.nan)
        columns = df.columns
        rows = df[[columns[0]]].index
        for column in columns:
            for row in range(len(rows)):
                data = df.loc[row, column]
                if data == '':
                    df.loc[row, column] = 0
        df_json = df.to_json(orient="split")
        return df_json


@shared_task()
def create_collection(customer_input_code, customer_code, url):
    customer_input_database = CustomerInputDataset()
    customer_input_json = customer_input_database.create_collection(
        url, customer_input_code)
    test_collection = TestCollection()
    test_collection.save_customer_with_gridfs(str(customer_input_json), customer_input_code)
        

