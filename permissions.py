from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return bool(request.user and request.user.is_authenticated)
