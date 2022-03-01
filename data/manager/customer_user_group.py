from django.db import IntegrityError, models
from data.utils.constant import Status
from data.utils.exceptions import DuplicatedRecord, InvalidOperation


class CustomerUserGroupQuerySet(models.QuerySet):
    def get_all(self):
        return self.filter(status=Status.ACTIVE.value)

    def get_customer_user_group_by_code(self, customer_user_group_code):
        return self.filter(status=Status.ACTIVE.value, customer_user_group_code=customer_user_group_code).first()

    def get_user_from_customer_group(self, user_code, customer_code):
        return self.filter(status=Status.ACTIVE.value, customer=customer_code, user=user_code)


class CustomerUserGroupManager(models.Manager):

    def get_queryset(self):
        return CustomerUserGroupQuerySet(self.model, using=self._db)

    def save(self, customer_user_group):
        try:
            customer_user_group.save()
            return customer_user_group
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save customer user group \n Error Mesage: {ex}"
            )

    def get_all_customer_user_group(self):
        return self.get_queryset().get_all()

    def get_customer_user_group_by_code(self, customer_user_group_code):
        return self.get_queryset().get_customer_user_group_by_code(customer_user_group_code)

    def check_user_membership(self, user_code, customer_code):
        membership = self.get_queryset().get_user_from_customer_group(
            user_code, customer_code)
        if not membership:
            return False
        else:
            return True
