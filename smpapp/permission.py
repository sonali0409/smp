# permissions.py
from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'seller'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'customer'
