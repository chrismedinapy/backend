import uuid
from django.db import models
from data.manager import product_input
from data.models.update_created import UpdatedCreated


class ProductInput(UpdatedCreated):
    product_input_code = models.UUIDField(primary_key= True, default =str (uuid.uuid4()))
    status = models.IntegerField()
    product_input_description = models.CharField(max_length=500)
    cvs_location = models.CharField(max_length=1000, blank=True, null=True)
    
    objects = product_input.ProductInputManager()

