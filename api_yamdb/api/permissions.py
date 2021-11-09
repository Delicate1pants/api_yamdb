
from rest_framework import permissions
from reviews.models import User


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        is_safe_method = request.method in permissions.SAFE_METHODS
        is_admin = request.user.is_authenticated and request.user.role == 'admin'
        return is_safe_method or is_admin