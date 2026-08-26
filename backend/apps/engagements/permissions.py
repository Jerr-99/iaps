from rest_framework.permissions import BasePermission


class EngagementPermission(BasePermission):
    """
    RBAC for the IAPS Engagements module.

    Administrator:
        Full access.

    Audit Supervisor:
        Full access.

    Auditor:
        Can view and create engagements.
        Cannot update or delete engagements.

    Finance Manager:
        No Engagements module access.
    """

    message = (
        "You do not have permission to perform this action "
        "on audit engagement records."
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
            ]

        # Finance Manager
        return False
