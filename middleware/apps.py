from django.apps import AppConfig


class Middleware(AppConfig):
    name = "middleware"

    def ready(self):
        # Register drf-spectacular extensions for the custom authentication class.
        from middleware.security import schema  # noqa: F401
