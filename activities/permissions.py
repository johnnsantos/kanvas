from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from rest_framework import status


class CreateActivityPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and not request.user.is_superuser and not request.user.is_staff:
            return True
        
        if request.method == 'POST' and request.user.is_superuser or request.user.is_staff:
            validation_error = ValidationError(detail='You dont have permissions')
            validation_error.status_code = status.HTTP_401_UNAUTHORIZED
            raise validation_error
        
        if request.method == 'PUT' and request.user.is_superuser or request.user.is_staff:
            return True
        
        if request.method == 'GET':
            return True

        return False
