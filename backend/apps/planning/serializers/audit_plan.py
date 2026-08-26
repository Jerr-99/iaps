"""
Serializer for IAPS audit plans.
"""

from rest_framework import serializers

from apps.planning.models import AuditPlan


class AuditPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for audit plans.

    RBAC workflow:
        Administrator:
            Full access, including approval/completion.

        Audit Supervisor:
            Full access, including approval/completion.

        Auditor:
            Can create and update planning records,
            but cannot approve or complete an audit plan.

        Finance Manager:
            No Planning access.
    """

    engagement_code = serializers.CharField(
        source="engagement.engagement_code",
        read_only=True,
    )

    prepared_by_username = serializers.CharField(
        source="prepared_by.username",
        read_only=True,
    )

    reviewed_by_username = serializers.CharField(
        source="reviewed_by.username",
        read_only=True,
    )

    procedures_count = serializers.IntegerField(
        source="procedures.count",
        read_only=True,
    )

    recommendations_count = serializers.IntegerField(
        source="ai_recommendations.count",
        read_only=True,
    )

    class Meta:
        model = AuditPlan

        fields = [
            "id",
            "engagement",
            "engagement_code",
            "title",
            "objectives",
            "scope",
            "status",
            "prepared_by",
            "prepared_by_username",
            "reviewed_by",
            "reviewed_by_username",
            "planned_start_date",
            "planned_end_date",
            "procedures_count",
            "recommendations_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "engagement_code",
            "prepared_by",
            "prepared_by_username",
            "reviewed_by",
            "reviewed_by_username",
            "procedures_count",
            "recommendations_count",
        ]

    def validate(self, attrs):
        """
        Enforce Planning workflow restrictions.

        Auditors may modify planning records but may not
        approve or complete an audit plan.
        """

        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return attrs

        user = request.user

        new_status = attrs.get("status")

        if new_status in ["approved", "completed"]:
            if user.role not in [
                user.ROLE_ADMIN,
                user.ROLE_SUPERVISOR,
            ]:
                raise serializers.ValidationError(
                    {
                        "status": (
                            "Only an Administrator or Audit Supervisor "
                            "can approve or complete an audit plan."
                        )
                    }
                )

        return attrs
