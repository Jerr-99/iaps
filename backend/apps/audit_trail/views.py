from rest_framework import viewsets

from apps.audit_trail.models import AuditLog
from apps.audit_trail.serializers import AuditLogSerializer
from apps.audit_trail.permissions import CanViewAuditLogs


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for audit logs.

    Audit logs are immutable and should normally be created
    automatically by the system.

    Supported filters:

        ?module=documents
        ?action=upload
        ?object_type=Document
        ?object_id=5
        ?user=1

    Filters can be combined.
    """

    queryset = AuditLog.objects.select_related(
        "user",
    ).all()

    serializer_class = AuditLogSerializer

    permission_classes = [
        CanViewAuditLogs,
    ]

    def get_queryset(self):
        """
        Return audit logs filtered by query parameters.
        """

        queryset = super().get_queryset()

        module = self.request.query_params.get(
            "module"
        )

        action = self.request.query_params.get(
            "action"
        )

        object_type = self.request.query_params.get(
            "object_type"
        )

        object_id = self.request.query_params.get(
            "object_id"
        )

        user_id = self.request.query_params.get(
            "user"
        )

        if module:
            queryset = queryset.filter(
                module=module
            )

        if action:
            queryset = queryset.filter(
                action=action
            )

        if object_type:
            queryset = queryset.filter(
                object_type=object_type
            )

        if object_id:
            queryset = queryset.filter(
                object_id=object_id
            )

        if user_id:
            queryset = queryset.filter(
                user_id=user_id
            )

        return queryset.order_by(
            "-created_at"
        )