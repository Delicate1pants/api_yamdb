from rest_framework import permissions


class HasAccessOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or user.is_authenticated
            and user.role in (
                user.roles.user, user.roles.moderator, user.roles.admin
            )
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == user
            or user.role in (user.roles.moderator, user.roles.admin)
        )


class IsOwnerOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        role = user.role
        return (
            role in (user.roles.moderator, user.roles.admin)
            or user.is_superuser
            or request.method in ['GET', 'PATCH']
            and role == user.roles.user
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = user.role
        return (
            role == user.roles.admin or user.is_superuser
            or obj == user
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and (
                user.role == user.roles.admin
                or user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.role == user.roles.admin
            or user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or user.is_authenticated
            and user.role == user.roles.admin
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or user.role == user.roles.admin
        )
