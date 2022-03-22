from rest_framework import serializers


class CustomerInputSerializers(serializers.Serializer):
    customer_input_description = serializers.CharField(max_length=1000)
