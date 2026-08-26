from rest_framework.permissions import BasePermission


class CanViewAuditLogs(BasePermission):
    """
    Allow access to audit logs only to users with
    the Django view_auditlog permission.

    Superusers are automatically allowed.
    """

    message = "You do not have permission to view audit logs."

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.user.has_perm(
            "audit_trail.view_auditlog"
        )