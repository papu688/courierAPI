from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'  
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender

class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'courier'

    def has_object_permission(self, request, view, obj):
        # Couriers can update and upload proof for parcels assigned to them
        return request.user == obj.courier

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

