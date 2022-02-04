import uuid

from django.forms import model_to_dict
from data.models.product import Product

from data.utils.constant import Status
from data.utils.exceptions import EntityNotFound


class ProductLogic():
    def __init__(self):
        self.fields = ['product_code', 'product_name', 'product_description']

    def create(self, product_data):
        product_code = str(uuid.uuid4())
        product_name = product_data.get("product_name")
        product_description = product_data.get("product_description")
        status = Status.ACTIVE.value

        new_product = Product(product_code=product_code, product_name=product_name,
                              product_description=product_description, status=status
                              )
        new_product_saved = Product.objects.save(new_product)

    def get_products(self):
        products = Product.objects.get_all_product()
        if not products:
            raise EntityNotFound(
                f"There are no products!"
            )
        product_list = []
        for product in products:
            product_list.append(self.__product_mapped(product))
        return product_list

    def get_product_by_code(self, product_code):
        product = Product.objects.get_product_by_code(product_code)
        if not product:
            raise EntityNotFound(
                f"There are no product with code {product_code}"
            )
        product_dict = self.__product_mapped(product)
        return product_dict

    def update(self, product_code, product_data):
        product = Product.objects.get_product_by_code(product_code)
        if not product:
            raise EntityNotFound(
                f"There are no product with code {product_code}"
            )
        product.product_name = product_data.get("product_name")
        product.product_description = product_data.get("product_description")
        product_save = Product.objects.save(product)
        return self.__product_mapped(product_save)

    def delete(self, product_code):
        product = Product.objects.get_product_by_code(product_code)
        if not product:
            raise EntityNotFound(
                f"There is no product with code {product_code}"
            )
        product.status = Status.INACTIVE.value
        Product.objects.save(product)

    def __product_mapped(self, product):
        product_dict = model_to_dict(product, fields=self.fields)
        product_dict['product_code'] = str(product.product_code)
        return product_dict
