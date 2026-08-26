"""
Serializer for IAPS audit procedures.
"""

from rest_framework import serializers

from apps.planning.models import AuditProcedure


class AuditProcedureSerializer(serializers.ModelSerializer):
    """
    Serializer for individual audit procedures.
    """

    audit_plan_title = serializers.CharField(
        source="audit_plan.title",
        read_only=True,
    )

    risk_area = serializers.CharField(
        source="risk.risk_area",
        read_only=True,
    )

    assigned_to_username = serializers.CharField(
        source="assigned_to.username",
        read_only=True,
    )

    class Meta:
        model = AuditProcedure

        fields = [
            "id",
            "audit_plan",
            "audit_plan_title",
            "risk",
            "risk_area",
            "name",
            "description",
            "procedure_type",
            "objective",
            "status",
            "priority",
            "assigned_to",
            "assigned_to_username",
            "planned_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "audit_plan_title",
            "risk_area",
            "assigned_to_username",
        ]