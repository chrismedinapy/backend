"""Small Celery tasks used only by the automated integration pipeline."""

import json
import os

from redis import Redis

from core.celery import app


def _redis_client():
    return Redis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        db=1,
        decode_responses=True,
    )


@app.task(name="core.ci_healthcheck", ignore_result=True)
def ci_healthcheck(value: str, marker_key: str) -> None:
    """Record deterministic proof that a real Celery worker executed the task."""

    client = _redis_client()
    payload = {
        "received": value,
        "status": "processed",
    }
    client.set(marker_key, json.dumps(payload, sort_keys=True), ex=60)
    client.close()


@app.task(
    bind=True,
    name="core.ci_retry_probe",
    ignore_result=True,
    max_retries=2,
)
def ci_retry_probe(self, marker_key: str) -> None:
    """Fail once, retry through RabbitMQ, then persist deterministic proof."""

    attempts_key = f"{marker_key}:attempts"
    client = _redis_client()
    attempts = client.incr(attempts_key)
    client.expire(attempts_key, 60)

    if attempts == 1:
        client.close()
        raise self.retry(
            exc=RuntimeError("intentional first-attempt CI failure"),
            countdown=0,
        )

    payload = {
        "attempts": attempts,
        "status": "recovered",
    }
    client.set(marker_key, json.dumps(payload, sort_keys=True), ex=60)
    client.close()
