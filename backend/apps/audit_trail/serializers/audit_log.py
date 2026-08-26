"""
Serializer for the IAPS audit trail.
"""

from rest_framework import serializers

from apps.audit_trail.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    """
    Read-oriented serializer for immutable audit logs.
    """

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = AuditLog

        fields = [
            "id",
            "user",
            "username",
            "action",
            "module",
            "object_type",
            "object_id",
            "description",
            "old_values",
            "new_values",
            "ip_address",
            "user_agent",
            "request_id",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "username",
            "created_at",
        ]