
from rest_framework import permissions
from reviews.models import User


class IsAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        is_admin = request.user.is_authenticated and request.user.role == 'admin'
        return is_admin

