"""
Serializers for IAPS risk assessments.
"""

from rest_framework import serializers

from apps.risk.models import Risk


class RiskSerializer(serializers.ModelSerializer):
    """
    Serializer for IAPS risk assessments.

    Workflow RBAC:

        Administrator:
            Can create any valid status.

        Audit Supervisor:
            Can create any valid status.

        Auditor:
            Can create only draft or assessed risks.

        Finance Manager:
            Blocked by RiskPermission.
    """

    # --------------------------------------------------------------
    # Related display fields
    # --------------------------------------------------------------

    engagement_code = serializers.CharField(
        source="engagement.engagement_code",
        read_only=True,
    )

    assessed_by_username = serializers.CharField(
        source="assessed_by.username",
        read_only=True,
    )

    reviewed_by_username = serializers.CharField(
        source="reviewed_by.username",
        read_only=True,
    )

    # --------------------------------------------------------------
    # Meta
    # --------------------------------------------------------------

    class Meta:
        model = Risk

        fields = [
            "id",

            # Engagement
            "engagement",
            "engagement_code",

            # Users
            "assessed_by",
            "assessed_by_username",
            "reviewed_by",
            "reviewed_by_username",

            # Risk identification
            "risk_area",
            "assertion",
            "risk_description",
            "risk_factors",

            # Inherent risk
            "inherent_risk_score",
            "inherent_risk_level",

            # Control risk
            "control_risk_score",
            "control_risk_level",

            # ROMM
            "romm_score",
            "romm_level",

            # Additional risk indicators
            "fraud_risk",
            "fraud_risk_score",
            "anomaly_detected",
            "anomaly_score",

            # Auditor assessment
            "auditor_assessment",
            "recommended_response",

            # Workflow
            "status",

            # Timestamps
            "created_at",
            "updated_at",
            "assessed_at",
            "reviewed_at",
        ]

        read_only_fields = [
            "id",
            "inherent_risk_level",
            "control_risk_level",
            "romm_score",
            "romm_level",
            "created_at",
            "updated_at",
            "assessed_by_username",
            "reviewed_by_username",
            "engagement_code",
        ]

    # --------------------------------------------------------------
    # Workflow validation
    # --------------------------------------------------------------

    def validate(self, attrs):
        """
        Enforce Risk workflow restrictions during creation.
        """

        request = self.context.get("request")

        if request is None:
            return attrs

        user = getattr(request, "user", None)

        if user is None or not user.is_authenticated:
            return attrs

        # Only apply creation workflow rules.
        if self.instance is not None:
            return attrs

        new_status = attrs.get("status")

        # Auditor may only create draft or assessed risks.
        if user.role == user.ROLE_AUDITOR:

            if new_status in {"reviewed", "approved"}:
                raise serializers.ValidationError(
                    {
                        "status": (
                            "Auditors can only create risk assessments "
                            "with draft or assessed status. "
                            "Only an Administrator or Audit Supervisor "
                            "can create reviewed or approved "
                            "risk assessments."
                        )
                    }
                )

        return attrs