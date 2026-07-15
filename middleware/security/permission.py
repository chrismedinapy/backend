from rest_framework.permissions import BasePermission


class CorePermission(BasePermission):
    """Allow requests whose JWT was validated against an active user."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.get("user_code"))
