from unittest.util import _MAX_LENGTH
from rest_framework import serializers


class CustomerInputSerializers(serializers.Serializer):
    customer_input_description = serializers.CharField(max_length=1000)
    customer_input_name = serializers.CharField(max_length=1000)
