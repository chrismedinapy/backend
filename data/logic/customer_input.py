import logging
import uuid
from django.conf import settings
from django.forms import model_to_dict
from data import models
from data.manager.test_mongo import TestCollection
from data.task.create_hash import hash_file
from data.task.create_customer_input_dataset import create_collection
from data.utils.constant import Status
from data.utils.exceptions import DuplicatedRecord,EntityNotFound
from data.utils.upload_file import upload_file_to_local


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
            test_collection = TestCollection()
            customer_gridfs_code = customer_queryset[0].gridfs_code
            customer_json = test_collection.list_customer_input_with_gridfs(
                customer_code, customer_gridfs_code)
            return customer_json
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