from rest_framework.permissions import BasePermission


class CreateActivityPermission(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method == "POST"
            or request.method == "GET"
            and not request.user.is_superuser
            and not request.user.is_staff
        ):
            return True
        if (
            request.method == "PUT"
            and request.user.is_superuser
            or request.user.is_staff
        ):
            return True
