
from rest_framework import permissions
from reviews.models import User


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated