from re import I
from django.db import IntegrityError, models
from data.utils.constant import Status

from data.utils.exceptions import DuplicatedRecord, InvalidOperation


class RetailStoreQuerySet(models.QuerySet):
    pass

    def get_all_by_customer_code(self, customer_code):
        return self.filter(status=Status.ACTIVE.value, customer=customer_code)


class RetailStoreManager(models.Manager):
    def get_queryset(self):
        return RetailStoreQuerySet(self.model, using=self._db)

    def save(self, retail_store):
        try:
            retail_store.save()
            return retail_store
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save retail store \n Error Message: {ex}"
            )

    def get_all_by_customer_code(self, customer_code):
        return self.get_queryset().get_all_by_customer_code(customer_code)
