from django.db import IntegrityError, models
from data.utils.constant import Status
from data.utils.exceptions import DuplicatedRecord, InvalidOperation


class ProductQuerySet(models.QuerySet):

    def get_all(self):
        return self.filter(status=Status.ACTIVE.value)

    def get_by_product_code(self, product_code):
        return self.filter(status=Status.ACTIVE.value, product_code=product_code).first()


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

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
