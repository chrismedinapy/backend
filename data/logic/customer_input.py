import logging
import uuid
from django.conf import settings

from django.forms import model_to_dict
from data import models
from data.manager.customer_input import CustomerInputManager
from data.manager.test_mongo import TestCollection
from data.utils.constant import Status
#from data.utils.mongo_client import MongoConnection
from data.utils.upload_file import upload_file_to_local


class CustomerInputLogic():
    def __init__(self):
        self.fields = ['customer_input_description',
                       'customer_input_code', 'customer_input_name']
        self.root_customer_input_dir = f'{settings.FILES_ROOT}/customer_csv'

    def create(self, customer_data, customer_csv, customer_code):

        customer_input_description = customer_data.get(
            'customer_input_description')
        customer_input_name = customer_data.get("customer_input_name")
        try:
            # create customer
            customer_input = models.CustomerInput(customer_input_code=str(uuid.uuid4()),
                                                  customer_input_description=customer_input_description, customer_input_name=customer_input_name, status=Status.ACTIVE.value)
            models.CustomerInput.objects.save(customer_input)

            # upload customer profile
            customer_input_code = str(customer_input.customer_input_code)
            url = self.__upload_csv(
                customer_input_name, customer_csv, customer_code)

            # update profile url to customer model
            customer_input.cvs_location = url
            models.CustomerInput.objects.save(customer_input)

            # Prueba de conexion a mongodb
            customer_input_mapped = self.__customer_input_mapped(
                customer_input)
            return customer_input_mapped
        except Exception as ex:
            logging.exception(
                f"Error while trying to save customer", exc_info=ex)
            raise ex

    def __customer_input_mapped(self, customer_input):
        customer_dict = model_to_dict(customer_input, fields=self.fields)
        customer_dict['customer_code'] = str(
            customer_input.customer_input_code)
        return customer_dict

    def __upload_csv(self, customer_input_name, file_csv, customer_code):
        local_path = upload_file_to_local(
            file_csv, f'{self.root_customer_input_dir}/{customer_code}/{customer_input_name}')
        return local_path
