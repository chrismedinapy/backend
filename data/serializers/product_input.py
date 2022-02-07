from unittest.util import _MAX_LENGTH
from rest_framework import serializers


class ProductInputSerializers(serializers.Serializer):
    product_input_description = serializers.CharField(max_length=1000)
