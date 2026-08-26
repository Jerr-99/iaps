from rest_framework.permissions import BasePermission


class CanManageUsers(BasePermission):
    """
    Allow only IAPS Administrators to manage users.
    """

    message = "You do not have permission to manage users."

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.user.can_manage_users()
