"""Serializers for IAPS Planning app."""

from rest_framework import serializers

from .models import (
    AIRecommendation,
    AuditPlan,
    AuditProcedure,
)


class AuditPlanSerializer(serializers.ModelSerializer):
    engagement_code = serializers.CharField(
        source="engagement.engagement_code",
        read_only=True,
    )

    prepared_by_username = serializers.CharField(
        source="prepared_by.username",
        read_only=True,
    )

    class Meta:
        model = AuditPlan
        fields = "__all__"
        read_only_fields = [
            "prepared_by",
            "reviewed_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        user = self.context["request"].user

        # Only Administrator and Supervisor can approve,
        # complete, or otherwise finalize a plan.
        if "status" in attrs:
            new_status = attrs["status"]

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


class AuditProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditProcedure
        fields = "__all__"

        read_only_fields = [
            "created_at",
            "updated_at",
        ]


class AIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecommendation
        fields = "__all__"

        read_only_fields = [
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]
