"""Small Celery tasks used only by the automated integration pipeline."""

from core.celery import app


@app.task(name="core.ci_healthcheck")
def ci_healthcheck(value: str) -> dict[str, str]:
    """Return a deterministic payload after execution by a real Celery worker."""

    return {
        "received": value,
        "status": "processed",
    }
