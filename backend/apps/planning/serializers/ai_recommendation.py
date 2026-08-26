"""
Serializer for IAPS AI-assisted audit recommendations.
"""

from rest_framework import serializers

from apps.planning.models import AIRecommendation


class AIRecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for AI-generated audit recommendations.

    AI recommendations remain subject to auditor review.
    """

    audit_plan_title = serializers.CharField(
        source="audit_plan.title",
        read_only=True,
    )

    risk_area = serializers.CharField(
        source="risk.risk_area",
        read_only=True,
    )

    reviewed_by_username = serializers.CharField(
        source="reviewed_by.username",
        read_only=True,
    )

    class Meta:
        model = AIRecommendation

        fields = [
            "id",
            "audit_plan",
            "audit_plan_title",
            "risk",
            "risk_area",
            "recommendation_type",
            "recommendation",
            "rationale",
            "confidence_score",
            "model_name",
            "status",
            "reviewed_by",
            "reviewed_by_username",
            "reviewer_notes",
            "created_at",
            "reviewed_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "reviewed_at",
            "audit_plan_title",
            "risk_area",
            "reviewed_by_username",
        ]

    def validate_confidence_score(self, value):
        """
        Ensure AI confidence remains between 0 and 100.
        """

        if value is not None and not 0 <= value <= 100:
            raise serializers.ValidationError(
                "Confidence score must be between 0 and 100."
            )

        return value