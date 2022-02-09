from rest_framework import serializers


class CustomerSerializers(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100)
    customer_description = serializers.CharField(max_length=200)
