"""Regression tests for serializer-backed request body validation."""

from uuid import uuid4

from django.test import SimpleTestCase
from rest_framework import serializers

from data.utils.exceptions import InvalidParameter
from data.utils.validator import body_validator


class SensitiveInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class NormalizedInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class BodyValidatorTests(SimpleTestCase):
    def test_returns_write_only_fields_for_business_logic(self):
        password_value = uuid4().hex
        payload = body_validator(
            {"username": "frontend", "password": password_value},
            SensitiveInputSerializer,
        )

        self.assertEqual(payload["username"], "frontend")
        self.assertEqual(payload["password"], password_value)

    def test_returns_normalized_validated_values_and_rejects_invalid_input(self):
        payload = body_validator({"quantity": "2"}, NormalizedInputSerializer)

        self.assertEqual(payload["quantity"], 2)
        with self.assertRaises(InvalidParameter):
            body_validator({"quantity": "0"}, NormalizedInputSerializer)
