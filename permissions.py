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
