from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.usertype == 1

class IsISP(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.usertype == 2

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.usertype == 3
    
class IsAdminOrISP(permissions.BasePermission):
    def has_permission(self, request, view):
        # Assuming usertype of 1 is Admin and 2 is ISP
        return request.user.is_authenticated and request.user.usertype in [1, 2]