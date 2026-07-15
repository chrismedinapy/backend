"""Celery task discovery entrypoint for the data application.

Celery's Django autodiscovery looks for a ``tasks`` module in installed apps.
The production task implementations remain grouped under ``data.task`` and are
re-exported here so a normal worker startup registers them deterministically.
"""

from data.task.create_customer_input_dataset import create_collection

__all__ = ("create_collection",)
