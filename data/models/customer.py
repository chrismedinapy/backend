import uuid
from data.manager import customer
from data.models.update_created import UpdatedCreated
from django.db import models


class Customer(UpdatedCreated):
    customer_code = models.UUIDField(default=str(
        uuid.uuid4()), primary_key=True, null=False, blank=False)
    customer_name = models.CharField(max_length=200)
    customer_description = models.TextField(max_length=1000)
    status = models.IntegerField()
    
    objects = customer.CustomerManager()
    