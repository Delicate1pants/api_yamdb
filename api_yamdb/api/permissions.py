from rest_framework import permissions


class HasAccessOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role in ('user', 'moderator', 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ('moderator', 'admin')
        )


class IsOwnerOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user = request.user
        role = user.role
        if role in ['admin', 'moderator'] or user.is_superuser:
            return True
        if request.method in ['GET', 'PATCH'] and role == 'user':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        role = request.user.role
        if role == 'admin' or request.user.is_superuser:
            return True
        return obj == request.user


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False
