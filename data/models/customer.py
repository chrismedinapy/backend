import uuid

from data.manager.customer import CustomerManager 
from data.manager.customer_user_group import CustomerUserGroupManager
from data.models.update_created import UpdatedCreated
from data.models.user import User
from django.db import models
from data.models.user import User
from django.db import models

class Customer(UpdatedCreated):
    customer_code = models.UUIDField(default=str(
        uuid.uuid4()), primary_key=True, null=False, blank=False)
    customer_name = models.CharField(max_length=200)
    customer_description = models.TextField(max_length=1000)
    status = models.IntegerField()
    users = models.ManyToManyField(
        User, through='CustomerUserGroup')

    objects = CustomerManager()

class CustomerUserGroup(UpdatedCreated):
    customer_user_group_code = models.UUIDField(default=str(
        uuid.uuid4()), primary_key=True, null=False, blank=False, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    date_join = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()
    user_access_level = models.IntegerField()

    objects = CustomerUserGroupManager()
