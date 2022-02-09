import uuid
from django.db import models
from data.manager import customer_input
from data.models.update_created import UpdatedCreated


class CustomerInput(UpdatedCreated):
    customer_input_code = models.UUIDField(primary_key= True, default =str (uuid.uuid4()))
    customer_input_name = models.CharField(max_length=500)
    status = models.IntegerField()
    customer_input_description = models.CharField(max_length=500)
    cvs_location = models.CharField(max_length=1000, blank=True, null=True)
    
    objects = customer_input.CustomerInputManager()

