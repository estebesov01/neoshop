from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsSupplierAndIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool((request.user and request.user.is_staff) and (obj.user == request.user))

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)