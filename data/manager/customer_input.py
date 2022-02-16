from django.db import models, IntegrityError
from data.utils.constant import Status
from data.utils.exceptions import DuplicatedRecord, InvalidOperation


class CustomerInputQuerySet(models.QuerySet):

    def get_all(self):
        return self.filter(status=Status.Active.value)

    def get_by_code(self, customer_input_code):
        return self.filter(status=Status.ACTIVE.value, customer_input_code=customer_input_code).first()

    def get_all_by_customer_code(self, customer_code):
        return self.filter(status=Status.ACTIVE.value, customer_code=customer_code)

    def get_by_customer_code_gridfs_code(self, customer_code, gridfs_code):
        return self.filter(status=Status.ACTIVE.value, customer_code=customer_code, gridfs_code=gridfs_code).first()


class CustomerInputManager(models.Manager):

    def get_queryset(self):
        return CustomerInputQuerySet(self.model, using=self._db)

    def get_customer_input_by_code(self, customer_input_code):
        return self.get_queryset().get_by_code(customer_input_code)

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

    def get_customer_input_by_customer_code_and_gridfs_code(self, customer_code, gridfs_code):
        return self.get_queryset().get_by_customer_code_gridfs_code(customer_code, gridfs_code)

    def get_all_product(self):
        return self.get_queryset().get_all()

    def get_all_by_customer_code(self, customer_code):
        return self.get_queryset().get_all_by_customer_code(customer_code)
