"""
Serializers for IAPS financial data.
"""

from rest_framework import serializers

from apps.financial.models import FinancialData


class FinancialDataSerializer(serializers.ModelSerializer):
    """
    Serializer for financial transaction records.
    """

    engagement_code = serializers.CharField(
        source="engagement.engagement_code",
        read_only=True,
    )

    imported_by_username = serializers.CharField(
        source="imported_by.username",
        read_only=True,
    )

    class Meta:
        model = FinancialData

        fields = [
            "id",
            "engagement",
            "engagement_code",
            "transaction_id",
            "transaction_date",
            "department",
            "expense_category",
            "vendor_supplier",
            "invoice_number",
            "transaction_amount",
            "budget_code",
            "payment_method",
            "approval_status",
            "payment_status",
            "transaction_description",
            "source_file",
            "imported_by",
            "imported_by_username",
            "imported_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "imported_at",
            "updated_at",
            "engagement_code",
            "imported_by_username",
        ]