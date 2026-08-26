"""
Serializers for the IAPS Engagements app.
"""

from rest_framework import serializers

from apps.engagements.models import Engagement


class EngagementSerializer(serializers.ModelSerializer):
    """
    Serializer for audit engagements.

    Provides both the user IDs used for relationships and
    read-only usernames for convenient API responses.
    """

    lead_auditor_username = serializers.CharField(
        source="lead_auditor.username",
        read_only=True,
    )

    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    financial_records_count = serializers.IntegerField(
        source="financial_data.count",
        read_only=True,
    )

    risks_count = serializers.IntegerField(
        source="risks.count",
        read_only=True,
    )

    audit_plans_count = serializers.IntegerField(
        source="audit_plans.count",
        read_only=True,
    )

    documents_count = serializers.IntegerField(
        source="documents.count",
        read_only=True,
    )

    class Meta:
        model = Engagement
        fields = [
            "id",
            "engagement_code",
            "title",
            "description",
            "department",
            "auditee",
            "audit_year",
            "start_date",
            "end_date",
            "status",
            "risk_level",
            "lead_auditor",
            "lead_auditor_username",
            "created_by",
            "created_by_username",
            "financial_records_count",
            "risks_count",
            "audit_plans_count",
            "documents_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "lead_auditor_username",
            "created_by_username",
            "financial_records_count",
            "risks_count",
            "audit_plans_count",
            "documents_count",
	    "lead_auditor",
            "created_by",
        ]

