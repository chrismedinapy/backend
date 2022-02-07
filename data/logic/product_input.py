import logging
from django.conf import settings

from django.forms import model_to_dict
from data import models
from data.utils.constant import Status
from data.utils.upload_file import upload_file_to_local

class ProductInputLogic():
    def __init__(self):
        self.fields = ['product_input_description', 'product_input_code']
        self.root_product_input_dir = f'{settings.FILES_ROOT}\\product_csv'

    def create(self, product_data, product_csv):
        product_input_description = product_data.get(
            'product_input_description')
        try:
            # create product
            product_input = models.ProductInput(
                product_input_description=product_input_description, status=Status.ACTIVE.value)
            models.ProductInput.objects.save(product_input)

            # upload product profile
            product_input_code = str(product_input.product_input_code)
            url = self.__upload_csv(product_input_code, product_csv)

            # update profile url to product model
            product_input.cvs_location = url
            models.ProductInput.objects.save(product_input)
            return self.__product_input_mapped(product_input)
        except Exception as ex:
            logging.exception(
                f"Error while trying to save product", exc_info=ex)
            raise ex

    def __product_input_mapped(self, product_input):
        product_dict = model_to_dict(product_input, fields=self.fields)
        product_dict['product_code'] = str(product_input.product_input_code)
        return product_dict

    def __upload_csv(self, product_input_code, file_csv):
        local_path = upload_file_to_local(
            file_csv, f'{self.root_product_input_dir}\\{product_input_code}')
        return local_path
