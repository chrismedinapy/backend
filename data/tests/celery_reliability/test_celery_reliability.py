import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

import gridfs
from bson.objectid import ObjectId
from django.db import close_old_connections
from django.test import TransactionTestCase
from pymongo.errors import ServerSelectionTimeoutError
from redis import Redis

from core.celery import app as celery_app
from core.ci_tasks import ci_retry_probe
from data.manager.mongo_connection import MongoCollection
from data.models.customer_input import CustomerInput
from data.task.create_customer_input_dataset import (
    _is_retryable,
    create_collection,
)
from data.utils.constant import Status
from data.utils.exceptions import InvalidOperation
from data.utils.mongo_client import get_client


class CeleryReliabilityTestCase(TransactionTestCase):
    reset_sequences = False

    def setUp(self):
        self.redis_client = Redis(
            host=os.environ.get("REDIS_HOST", "localhost"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            db=1,
            decode_responses=True,
        )

    def tearDown(self):
        self.redis_client.close()
        close_old_connections()

    def test_retry_probe_fails_once_and_recovers(self):
        marker_key = f"test:celery-retry:{uuid.uuid4().hex}"
        attempts_key = f"{marker_key}:attempts"
        self.redis_client.delete(marker_key, attempts_key)

        try:
            result = ci_retry_probe.apply(args=[marker_key], throw=False)
            self.assertTrue(result.successful(), result.result)

            payload = json.loads(self.redis_client.get(marker_key))
            self.assertEqual(
                payload,
                {"attempts": 2, "status": "recovered"},
            )
            self.assertEqual(int(self.redis_client.get(attempts_key)), 2)
        finally:
            self.redis_client.delete(marker_key, attempts_key)

    def test_production_task_has_bounded_transient_retry_policy(self):
        self.assertEqual(create_collection.max_retries, 3)
        self.assertIs(create_collection.acks_late, True)
        self.assertIs(create_collection.reject_on_worker_lost, True)

        transient_error = ServerSelectionTimeoutError("temporary MongoDB outage")
        wrapped_error = InvalidOperation("temporary persistence failure")
        wrapped_error.__cause__ = transient_error

        self.assertTrue(_is_retryable(wrapped_error))
        self.assertFalse(_is_retryable(ValueError("invalid CSV")))

    def test_no_scheduled_tasks_are_configured_without_a_ci_contract(self):
        self.assertEqual(celery_app.conf.beat_schedule or {}, {})

    def test_duplicate_deliveries_share_one_gridfs_object(self):
        customer_input_code = uuid.uuid4()
        customer_input = CustomerInput(
            customer_input_code=customer_input_code,
            customer_code=uuid.uuid4(),
            status=Status.ACTIVE.value,
            customer_input_description="Celery idempotency test",
        )
        customer_input.save()

        payload = json.dumps(
            {
                "columns": ["product", "quantity"],
                "data": [["coffee", "2"]],
            },
            sort_keys=True,
        )
        expected_object_id = MongoCollection._gridfs_object_id(
            customer_input_code
        )

        def persist_duplicate(_):
            close_old_connections()
            try:
                return str(
                    MongoCollection().save_customer_with_gridfs(
                        payload,
                        customer_input_code,
                    )
                )
            finally:
                close_old_connections()

        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                stored_codes = list(executor.map(persist_duplicate, range(4)))

            self.assertEqual(
                stored_codes,
                [str(expected_object_id)] * 4,
            )

            customer_input.refresh_from_db()
            self.assertEqual(
                customer_input.gridfs_code,
                str(expected_object_id),
            )

            database = get_client()
            self.assertEqual(
                database["fs.files"].count_documents(
                    {"_id": expected_object_id}
                ),
                1,
            )
            self.assertEqual(
                database["fs.files"].count_documents(
                    {
                        "metadata.customer_input_code": str(
                            customer_input_code
                        )
                    }
                ),
                1,
            )
        finally:
            database = get_client()
            fs = gridfs.GridFS(database)
            if fs.exists(ObjectId(expected_object_id)):
                fs.delete(ObjectId(expected_object_id))
            CustomerInput.objects.filter(
                customer_input_code=customer_input_code
            ).delete()
