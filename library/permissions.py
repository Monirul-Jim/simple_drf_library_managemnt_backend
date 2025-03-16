from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff


class IsLibrarianOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
