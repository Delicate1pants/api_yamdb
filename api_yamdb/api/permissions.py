
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method == 'GET' and request.user.is_authenticated and view.kwargs.get('username', None) == 'me':
            return True

        if request.method == 'PATCH' and request.user.is_authenticated and request.user.role == 'user' and view.kwargs.get('username', None) == 'me':
            return True
        
        is_admin = request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser)
        return is_admin

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser)
        if request.method == 'PATCH' and request.user.role == 'user' and view.kwargs.get('username', None) == 'me':
            return True
        return is_admin

class IsOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH' and request.user.role == 'user' and view.kwargs.get('username', None) == 'me':
            return True
        return request.user.is_authenticated or obj == request.user