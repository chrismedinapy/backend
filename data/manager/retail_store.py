from django.db import IntegrityError, models

from data.utils.exceptions import DuplicatedRecord, InvalidOperation


class RetailStoreQuerySet(models.QuerySet):
    pass


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
