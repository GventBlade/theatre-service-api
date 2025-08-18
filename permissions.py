from rest_framework import permissions


class IsAdminOrTicketBuyer(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated and request.method == "POST":
            return True

        return False


class IsAdminOrOwner(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj == request.user
