import logging
from re import A
import uuid
import json
from django.conf import settings
from django.forms import model_to_dict
from data import models
from data.manager.mongo_connection import MongoCollection
from data.task.create_hash import hash_file
from data.task.create_customer_input_dataset import create_collection
from data.utils.constant import Status
from data.utils.exceptions import DuplicatedRecord, EntityNotFound
from data.utils.upload_file import upload_file_to_local
from data.task.merge_dataframes import merge_dataframes


class CustomerInputLogic():
    def __init__(self):
        self.fields = ['customer_input_description',
                       'customer_input_code', 'customer_input_name']
        self.root_customer_input_dir = f'{settings.FILES_ROOT}/customer_csv'

    def create(self, customer_data, customer_csv, customer_code):

        customer_input_description = customer_data.get(
            'customer_input_description')
        try:
            customer_queryset = models.CustomerInput.objects.get_all_by_customer_code(
                customer_code)
            # create customer.
            customer_input = models.CustomerInput(customer_input_code=str(uuid.uuid4()),
                                                  customer_input_description=customer_input_description, customer_csv_uploaded_name=customer_csv.name,
                                                  customer_code=customer_code, customer_input_name=customer_data.get("customer_input_name"), status=Status.ACTIVE.value)
            # verify if the hash has already uploaded before.
            # TODO
            # Esto debe ir en una funcion asincrona,
            # debido a que los archivos pueden ser grandes y puden tardar mucho.
            hashed_csv = hash_file(customer_csv)
            # aumentamos el valor del csv_number.
            if customer_queryset:
                csv_count = len(customer_queryset) + 1
                customer_input.csv_number = csv_count
                for customer in customer_queryset:
                    if customer.csv_hash == hashed_csv:
                        raise DuplicatedRecord(f"File already uploaded!")
                    else:
                        customer_input.csv_hash = hashed_csv
            customer_input.csv_hash = hashed_csv
            models.CustomerInput.objects.save(customer_input)
            # get customer input code
            customer_input_code = str(customer_input.customer_input_code)
            file_name = 'archivo_'
            csv_count = customer_input.csv_number
            new_csv_name = f"archivo_{csv_count}.csv"
            # guardamos el archivo csv.
            url = self.__upload_csv(
                customer_csv, customer_code, new_csv_name)
            customer_input.csv_number = csv_count
            customer_input.csv_location = url
            customer_input.csv_name = new_csv_name

            models.CustomerInput.objects.save(customer_input)

            customer_input_mapped = self.__customer_input_mapped(
                customer_input)
            # guardamos los datos del archivo csv en la base de datos mongodb
            # Esta tarea es asincrona.
            create_collection.delay(customer_input_code, customer_code, url)

            return customer_input_mapped
        except Exception as ex:
            logging.exception(
                f"Error while trying to save customer", exc_info=ex)
            raise ex

    def list(self, customer_code):
        customer_queryset = models.CustomerInput.objects.get_all_by_customer_code(
            customer_code)
        if customer_queryset:
            if len(customer_queryset) == 1:
                gridfs = customer_queryset[0].gridfs_code
                return self.__convert_from_json_to_dict(self.__get_customer_json_by_gridfs_code(customer_code, gridfs))
            elif len(customer_queryset) >= 2:
                customer_gridfs_list = []
                for customer in customer_queryset:
                    customer_gridfs = customer.gridfs_code
                    customer_gridfs_list.append(customer_gridfs)
                customer_json_list = []
                for gridfs in customer_gridfs_list:
                    customer_aux = self.__get_customer_json_by_gridfs_code(
                        customer_code, gridfs)
                    customer_json_list.append(customer_aux)
                customer_json = customer_json_list[0]
                for x in range(len(customer_json_list)):
                    if x+1 < len(customer_json_list):
                        customer_json = merge_dataframes(
                            customer_json, customer_json_list[x+1])
                    else:
                        break
                aux = self.__convert_from_json_to_dict(customer_json)
                print("#"*50)
                print(len(aux))
                return aux
                # customer_gridfs_code = customer_queryset[0].gridfs_code
                # test_collection = MongoCollection()
                # customer_json = test_collection.list_customer_input_with_gridfs(
                # customer_code, customer_gridfs_code)
                # convertimos la coleccion de tipo json a una lista de diccionarios,
                # para su mejor representacion en la view.
                # customer_list = []
                # customer_columns = customer_json["columns"]
                # customer_index = customer_json["index"]
                # customer_data = customer_json["data"]
                # for i in range(len(customer_index)):
                #     customer = {}
                #     for x in range(len(customer_columns)):
                #         customer.update({customer_columns[x]: customer_data[i][x]})
                #     customer.update({"index": customer_index[i]})
                #     customer_list.append(customer)
                # return customer_list
        else:
            raise EntityNotFound(
                f"No customer data with customer_code: {customer_code}"
            )

    def __customer_input_mapped(self, customer_input):
        customer_dict = model_to_dict(customer_input, fields=self.fields)
        customer_dict['customer_code'] = str(
            customer_input.customer_input_code)
        return customer_dict

    def __upload_csv(self, file_csv, customer_code, new_csv_name):
        local_path = upload_file_to_local(
            file_csv, f'{self.root_customer_input_dir}/{customer_code}', new_csv_name)
        return local_path

    def __get_customer_json_by_gridfs_code(self, customer_code, gridfs_code):
        test_collection = MongoCollection()
        customer_json = test_collection.list_customer_input_with_gridfs(
            customer_code, gridfs_code)
        return customer_json

    def __convert_from_json_to_dict(self, customer_json):
        customer_columns = customer_json["columns"]
        customer_index = customer_json["index"]
        customer_data = customer_json["data"]
        customer_list = []
        for i in range(len(customer_index)):
            customer = {}
            for x in range(len(customer_columns)):
                customer.update({customer_columns[x]: customer_data[i][x]})
                customer.update({"index": customer_index[i]})
                customer_list.append(customer)
        return customer_list
