import uuid
from django.db import models
from data.manager import customer_input
from data.models.retail_store import RetailStore
from data.models.update_created import UpdatedCreated


class CustomerInput(UpdatedCreated):
    customer_input_code = models.UUIDField(
        primary_key=True, default=str(uuid.uuid4()))
    customer_code = models.UUIDField(blank=True, null=True)
    retail_store = models.ForeignKey(
        RetailStore, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField()
    customer_csv_uploaded_name = models.CharField(
        max_length=500, null=True, blank=True)
    customer_input_description = models.CharField(max_length=500)
    csv_location = models.CharField(max_length=1000, blank=True, null=True)
    csv_name = models.CharField(max_length=500, blank=True, null=True)
    csv_number = models.IntegerField(default=1)
    csv_hash = models.CharField(max_length=1000, blank=True, null=True)
    gridfs_code = models.CharField(max_length=100, blank=True, null=True)

    objects = customer_input.CustomerInputManager()
