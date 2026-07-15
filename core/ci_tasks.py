"""Small Celery tasks used only by the automated integration pipeline."""

import json
import os

from redis import Redis

from core.celery import app


@app.task(name="core.ci_healthcheck", ignore_result=True)
def ci_healthcheck(value: str, marker_key: str) -> None:
    """Record deterministic proof that a real Celery worker executed the task."""

    client = Redis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        db=1,
        decode_responses=True,
    )
    payload = {
        "received": value,
        "status": "processed",
    }
    client.set(marker_key, json.dumps(payload, sort_keys=True), ex=60)
    client.close()
