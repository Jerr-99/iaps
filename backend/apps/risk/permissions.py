from rest_framework.permissions import BasePermission


class RiskPermission(BasePermission):
    """
    RBAC for the IAPS Risk module.

    Administrator:
        Full access.

    Audit Supervisor:
        Full access.

    Auditor:
        View and create risk assessments.
        Cannot update or delete existing assessments.

    Finance Manager:
        No Risk module access.
    """

    message = (
        "You do not have permission to perform this action "
        "on risk assessments."
    )

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # ---------------------------------------------------------
        # Administrator
        # ---------------------------------------------------------

        if user.role == user.ROLE_ADMIN:
            return True

        # ---------------------------------------------------------
        # Audit Supervisor
        # ---------------------------------------------------------

        if user.role == user.ROLE_SUPERVISOR:
            return True

        # ---------------------------------------------------------
        # Auditor
        # ---------------------------------------------------------

        if user.role == user.ROLE_AUDITOR:
            return request.method in {
                "GET",
                "HEAD",
                "OPTIONS",
                "POST",
            }

        # ---------------------------------------------------------
        # Finance Manager / unknown roles
        # ---------------------------------------------------------

        return False