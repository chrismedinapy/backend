from rest_framework import serializers


class ProductSerializers(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    product_description = serializers.CharField(max_length=200)
