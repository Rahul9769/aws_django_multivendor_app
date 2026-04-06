from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vendor'

class IsVendorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'vendor'

class IsOwnerVendor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.vendor == request.user
