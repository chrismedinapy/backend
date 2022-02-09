from django.db import IntegrityError, models
from data.utils.constant import Status
from data.utils.exceptions import DuplicatedRecord, InvalidOperation


class CustomerQuerySet(models.QuerySet):
    def get_all(self):
        return self.filter(status=Status.ACTIVE.value)

    def get_by_customer_code(self, customer_code):
        return self.filter(status=Status.ACTIVE.value, customer_code=customer_code).first()


class CustomerManager(models.Manager):

    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def save(self, customer):
        try:
            customer.save()
            return customer
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save customer \n Error Mesage: {ex}"
            )

    def get_all_customer(self):
        return self.get_queryset().get_all()

    def get_customer_by_code(self, customer_code):
        return self.get_queryset().get_by_customer_code(customer_code)