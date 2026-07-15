from .celery import app as celery_app

# Expose the conventional ``app`` attribute so Celery's ``-A core`` CLI lookup
# resolves the project application deterministically in CI and local commands.
app = celery_app

__all__ = ("app", "celery_app")
