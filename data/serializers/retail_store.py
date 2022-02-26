from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField


class RetailStoreSerializers(serializers.Serializer):
    retail_store_name = serializers.CharField(max_length=100)
    retail_store_city = serializers.CharField(max_length=100)
    retail_store_location = PointField()
