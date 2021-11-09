
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        is_admin = request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser)
        return is_admin
