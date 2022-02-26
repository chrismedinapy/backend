from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from data.models.update_created import UpdatedCreated
from data.models.customer import Customer
from data.manager import retail_store

class RetailStore(UpdatedCreated):
    retail_store_code = models.UUIDField(primary_key=True)
    retail_store_name = models.CharField(max_length=1000)
    retail_store_location = models.PointField(geography=True, default=Point(0.0, 0.0))
    retail_store_city = models.CharField(max_length=500)
    status = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    objects = retail_store.RetailStoreManager()