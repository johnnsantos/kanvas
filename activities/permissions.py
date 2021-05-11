from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from rest_framework import status


class CreateActivityPermission(BasePermission):
    def has_permission(self, request, view):
        # se for criar precisa ser estudante
        if request.method == "POST":
            if (
                not request.user.is_superuser
                and not request.user.is_staff
                and request.user.is_authenticated
            ):
                return True
            else:
                validation_error = ValidationError(detail="You dont have permissions")
                validation_error.status_code = status.HTTP_401_UNAUTHORIZED
                raise validation_error

        # apenas facilitador ou instrutor pode usar PUT
        if request.method == "PUT":
            # se for estudante retorna 401
            if not request.user.is_superuser and not request.user.is_staff:
                validation_error = ValidationError(detail="You dont have permissions")
                validation_error.status_code = status.HTTP_401_UNAUTHORIZED
                raise validation_error
            else:
                return True

        if request.method == "GET":
            return True
