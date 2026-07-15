"""Regression tests for the validated retail-store location boundary."""

from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.contrib.gis.geos import Point
from django.test import SimpleTestCase

from data.logic.retail_store import RetailStoreLogic
from data.utils.exceptions import InvalidParameter


class RetailStoreLocationContractTests(SimpleTestCase):
    @patch("data.logic.retail_store.RetailStore.objects.save")
    @patch("data.logic.retail_store.Customer.objects.get_customer_by_code")
    def test_create_persists_the_validated_point_without_reparsing(
        self,
        get_customer,
        save_retail_store,
    ):
        customer = SimpleNamespace(customer_code=uuid4())
        point = Point(45.4545, 80.4545)
        get_customer.return_value = customer

        RetailStoreLogic().create(
            {
                "retail_store_name": "Store",
                "retail_store_city": "Limpio",
                "retail_store_location": point,
            },
            str(customer.customer_code),
        )

        saved = save_retail_store.call_args.args[0]
        self.assertIs(saved.retail_store_location, point)
        self.assertEqual(saved.retail_store_location.x, 45.4545)
        self.assertEqual(saved.retail_store_location.y, 80.4545)

    def test_create_rejects_unvalidated_location_values(self):
        with self.assertRaises(InvalidParameter):
            RetailStoreLogic().create(
                {
                    "retail_store_name": "Store",
                    "retail_store_city": "Limpio",
                    "retail_store_location": {
                        "longitude": 45.4545,
                        "latitude": 80.4545,
                    },
                },
                str(uuid4()),
            )
