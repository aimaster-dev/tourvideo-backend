from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 1

class IsISP(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 2

class IsClerk(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 3
    
class IsAdminOrISP(permissions.BasePermission):
    def has_permission(self, request, view):
        # Assuming user_type of 1 is Admin and 2 is Customer
        return request.user.is_authenticated and request.user.user_type in [1, 2]