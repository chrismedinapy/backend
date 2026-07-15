"""Standardized error responses for Django REST Framework and middleware."""

from http import HTTPStatus

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


DEFAULT_ERRORS = {
    400: ("invalid_parameter", "Invalid parameter"),
    401: ("authentication_required", "Authentication required"),
    403: ("permission_denied", "Permission denied"),
    404: ("not_found", "Resource not found"),
    409: ("conflict", "Request conflicts with the current resource state"),
    415: ("unsupported_media_type", "Unsupported media type"),
    500: ("internal_error", "Internal server error"),
}

LEGACY_ERROR_CODES = {
    0: "invalid_parameter",
    1: "invalid_token",
    2: "unauthorized",
    3: "not_found",
    4: "internal_error",
    5: "duplicated_record",
    6: "used_invitation",
    7: "members_exceeded",
    8: "not_owner",
    9: "unsupported_media_type",
    10: "not_member",
}


def _stringify(value):
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return [str(value)]


def _extract_fields(data):
    if not isinstance(data, dict):
        return {}

    fields = {}
    for field, value in data.items():
        if field in {"detail", "message", "error", "code"}:
            continue
        fields[field] = _stringify(value)
    return fields


def _resolve_code(exception, status_code):
    explicit_code = getattr(exception, "error_code", None)
    if isinstance(explicit_code, str):
        return explicit_code
    if explicit_code in LEGACY_ERROR_CODES:
        return LEGACY_ERROR_CODES[explicit_code]
    return DEFAULT_ERRORS.get(status_code, DEFAULT_ERRORS[500])[0]


def _resolve_message(exception, data, status_code):
    explicit_message = getattr(exception, "message", None)
    if explicit_message:
        return str(explicit_message)
    if isinstance(data, dict) and data.get("detail"):
        return str(data["detail"])
    if isinstance(data, str):
        return data
    return DEFAULT_ERRORS.get(status_code, DEFAULT_ERRORS[500])[1]


def error_payload(exception, status_code, data=None):
    """Build the stable frontend-facing error envelope."""
    return {
        "error": {
            "code": _resolve_code(exception, status_code),
            "message": _resolve_message(exception, data, status_code),
            "fields": _extract_fields(data),
        }
    }


def api_exception_handler(exception, context):
    """Normalize DRF and legacy application exceptions into one JSON contract."""
    response = drf_exception_handler(exception, context)

    if response is not None:
        response.data = error_payload(exception, response.status_code, response.data)
        return response

    status_code = getattr(exception, "status_code", None)
    if status_code is not None:
        return Response(
            error_payload(exception, status_code),
            status=status_code,
        )

    return None


def json_error_response(exception, status_code=500):
    """Return the same error envelope for exceptions handled by Django middleware."""
    if status_code not in DEFAULT_ERRORS:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return JsonResponse(error_payload(exception, int(status_code)), status=int(status_code))
