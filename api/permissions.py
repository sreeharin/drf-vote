from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    '''Allow read only permission for anonymous users'''
    def has_permission(self, request, view):
        if self.request.method in permissions.SAFE_METHODS:
            return True
        return False