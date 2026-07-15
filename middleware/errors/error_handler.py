"""Fallback exception middleware for errors outside DRF's exception flow."""

import logging

from middleware.errors.api_errors import json_error_response


logger = logging.getLogger(__name__)


class CoreErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.exception(
            "Unhandled request exception",
            extra={"path": request.path, "method": request.method},
        )

        status_code = getattr(exception, "status_code", 500)
        return json_error_response(exception, status_code=status_code)
