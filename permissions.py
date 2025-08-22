# Theatre/permissions.py

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access for all, but full access for admins.
    Suitable for public data like plays or halls.
    """
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAdminOrOwner(permissions.BasePermission):
    message = 'You do not have permission to access this page or object.'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        # Check if the user is the owner of the object.
        # This assumes the object has a 'user' or 'reservation.user' attribute.
        owner = getattr(obj, 'user', None) or getattr(obj.reservation, 'user', None)
        return owner == request.user
