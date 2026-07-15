"""Validate the real asynchronous CSV ingestion business flow in CI.

The script creates deterministic fixture records, calls the production REST
endpoint with a multipart CSV upload, waits for a separate Celery worker to
process the production task, and verifies the resulting PostgreSQL and MongoDB
GridFS state. It then publishes duplicate deliveries and proves that concurrent
workers converge on one deterministic GridFS object. All generated records and
files are removed before exit.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_ci")

import django

django.setup()

import gridfs
import jwt
from bson.objectid import ObjectId
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import close_old_connections
from rest_framework.test import APIClient

from data.models.customer import Customer
from data.models.customer_input import CustomerInput
from data.models.retail_store import RetailStore
from data.models.user import User
from data.task.create_customer_input_dataset import create_collection
from data.utils.constant import Status
from data.utils.mongo_client import get_client


TIMEOUT_SECONDS = 30
DUPLICATE_DELIVERIES = 4


def _create_token(user_code: uuid.UUID) -> str:
    payload = {
        "user_code": str(user_code),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=os.environ.get("ALGORITHM", "HS256"),
    )


def main() -> None:
    run_id = uuid.uuid4().hex[:12]
    user_code = uuid.uuid4()
    customer_code = uuid.uuid4()
    retail_store_code = uuid.uuid4()
    customer_input = None
    gridfs_code = None
    customer_files = (
        Path(settings.FILES_ROOT) / "customer_csv" / str(customer_code)
    )

    try:
        assert create_collection.max_retries == 3
        assert create_collection.acks_late is True
        assert create_collection.reject_on_worker_lost is True

        user = User(
            user_login_code=user_code,
            username=f"ci_{run_id}",
            password=uuid.uuid4().hex,
            name="CI asynchronous flow",
            email=f"ci-{run_id}@example.test",
            phone_number=f"+595{run_id}",
            status=Status.ACTIVE.value,
        )
        user.save()

        customer = Customer(
            customer_code=customer_code,
            customer_name=f"CI customer {run_id}",
            customer_description="Temporary customer for asynchronous CI validation",
            status=Status.ACTIVE.value,
        )
        customer.save()

        retail_store = RetailStore(
            retail_store_code=retail_store_code,
            retail_store_name=f"CI store {run_id}",
            retail_store_location=Point(0.0, 0.0),
            retail_store_city="CI",
            status=Status.ACTIVE.value,
            customer=customer,
        )
        retail_store.save()

        csv_content = (
            '"product","quantity"\n'
            '"coffee","2"\n'
            '"tea","3"\n'
        ).encode("utf-8")
        uploaded_csv = SimpleUploadedFile(
            "customer-products.csv",
            csv_content,
            content_type="text/csv",
        )

        client = APIClient()
        endpoint = (
            f"/data/customers/{customer_code}/retail-store/"
            f"{retail_store_code}/products/"
        )
        response = client.post(
            endpoint,
            data={
                "customer": json.dumps(
                    {
                        "customer_input_description": (
                            "CI asynchronous customer input"
                        )
                    }
                ),
                "customer_csv": uploaded_csv,
            },
            format="multipart",
            HTTP_AUTHORIZATION=f"Bearer {_create_token(user_code)}",
            HTTP_HOST="localhost",
        )
        assert response.status_code == 201, (
            f"CSV upload endpoint returned {response.status_code}: "
            f"{getattr(response, 'data', response.content)!r}"
        )

        customer_input = CustomerInput.objects.get_all_by_customer_code(
            customer_code
        ).get()
        assert customer_input.csv_hash, "CSV hash was not persisted"
        assert customer_input.csv_location, "CSV location was not persisted"
        assert Path(customer_input.csv_location).is_file(), (
            f"Uploaded CSV is missing at {customer_input.csv_location}"
        )

        deadline = time.monotonic() + TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            close_old_connections()
            customer_input.refresh_from_db()
            if customer_input.gridfs_code:
                gridfs_code = customer_input.gridfs_code
                break
            time.sleep(0.25)
        else:
            raise RuntimeError(
                "Production Celery task did not persist gridfs_code in PostgreSQL"
            )

        database = get_client()
        fs = gridfs.GridFS(database)
        object_id = ObjectId(gridfs_code)
        assert fs.exists(object_id), "Celery task did not persist the dataset in GridFS"

        stored_payload = fs.get(object_id).read()
        if isinstance(stored_payload, bytes):
            stored_payload = stored_payload.decode("utf-8")
        dataset = json.loads(stored_payload)

        assert dataset["columns"] == ["product", "quantity"], dataset
        assert dataset["data"] == [["coffee", "2"], ["tea", "3"]], dataset

        duplicate_results = [
            create_collection.delay(
                str(customer_input.customer_input_code),
                str(customer_code),
                customer_input.csv_location,
            )
            for _ in range(DUPLICATE_DELIVERIES)
        ]
        returned_codes = [
            result.get(timeout=TIMEOUT_SECONDS, propagate=True)
            for result in duplicate_results
        ]

        assert returned_codes == [str(object_id)] * DUPLICATE_DELIVERIES
        close_old_connections()
        customer_input.refresh_from_db()
        assert customer_input.gridfs_code == str(object_id)
        assert database["fs.files"].count_documents({"_id": object_id}) == 1
        assert database["fs.files"].count_documents(
            {
                "metadata.customer_input_code": str(
                    customer_input.customer_input_code
                )
            }
        ) == 1

        print(
            "Asynchronous customer-input reliability validated: "
            "HTTP upload -> PostgreSQL -> RabbitMQ -> concurrent Celery workers -> "
            "one idempotent MongoDB GridFS object -> PostgreSQL gridfs_code"
        )
    finally:
        cache.clear()

        if gridfs_code:
            try:
                gridfs.GridFS(get_client()).delete(ObjectId(gridfs_code))
            except Exception as exc:  # cleanup must not hide the primary failure
                print(f"GridFS cleanup warning: {exc}")

        if customer_input is not None:
            CustomerInput.objects.filter(
                customer_input_code=customer_input.customer_input_code
            ).delete()
        RetailStore.objects.filter(retail_store_code=retail_store_code).delete()
        Customer.objects.filter(customer_code=customer_code).delete()
        User.objects.filter(user_login_code=user_code).delete()
        shutil.rmtree(customer_files, ignore_errors=True)
        close_old_connections()


if __name__ == "__main__":
    main()
