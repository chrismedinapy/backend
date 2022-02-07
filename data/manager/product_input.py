from django.db import models, IntegrityError
from data.utils.constant import Status
from data.utils.exceptions import DuplicatedRecord, InvalidOperation



class ProductInputQuerySet(models.QuerySet):
    def get_all(self):
        return self.filter(status=Status.Active.value)

    def get_by_code(self, product_input_code):
        return self.filter(status=Status.Active.value, product_input_code=product_input_code)


class ProductInputManager(models.Manager):

    def get_queryset(self):
        return ProductInputQuerySet(self.model, using=self._db)

    def save(self, product):
        try:
            product.save()
            return product
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save product \n Error Mesage: {ex}"
            )

    def get_all_product(self):
        return self.get_queryset().get_all()

    def get_product_by_code(self, product_code):
        return self.get_queryset().get_by_product_code(product_code)
