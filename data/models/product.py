import uuid
from data.manager import product
from data.models.update_created import UpdatedCreated
from django.db import models


class Product(UpdatedCreated):
    product_code = models.UUIDField(default=str(
        uuid.uuid4()), primary_key=True, null=False, blank=False)
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(max_length=1000)
    status = models.IntegerField()
    
    objects = product.ProductManager()
    