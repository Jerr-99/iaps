from rest_framework.permissions import BasePermission


class PlanningPermission(BasePermission):
    """
    RBAC for the IAPS Planning module.

    Administrator:
        Full access.

    Audit Supervisor:
        Full access, including review and approval.

    Auditor:
        Can view, create, and update planning records.
        Cannot delete planning records.

    Finance Manager:
        No Planning module access.
    """

    message = (
        "You do not have permission to perform this action "
        "on audit planning records."
    )

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Administrator
        if user.role == user.ROLE_ADMIN:
            return True

        # Audit Supervisor
        if user.role == user.ROLE_SUPERVISOR:
            return True

        # Auditor
        if user.role == user.ROLE_AUDITOR:
            return request.method in [
                "GET",
                "HEAD",
                "OPTIONS",
                "POST",
                "PUT",
                "PATCH",
            ]

        # Finance Manager
        return False
