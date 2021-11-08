
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated