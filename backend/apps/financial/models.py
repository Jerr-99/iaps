"""
Models for the IAPS Financial app.

FinancialData stores financial transaction and budget information
associated with an audit engagement.
"""

import uuid

from django.conf import settings
from django.db import models


class FinancialData(models.Model):
    """
    Financial transaction record belonging to an audit engagement.

    These records form the primary financial dataset used by IAPS
    for financial analysis, anomaly detection, risk assessment,
    and audit planning.
    """

    PAYMENT_METHOD_CHOICES = (
        ("cash", "Cash"),
        ("cheque", "Cheque"),
        ("bank_transfer", "Bank Transfer"),
        ("electronic", "Electronic Payment"),
        ("other", "Other"),
    )

    APPROVAL_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
        ("failed", "Failed"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # Audit engagement
    engagement = models.ForeignKey(
        "engagements.Engagement",
        on_delete=models.CASCADE,
        related_name="financial_data",
    )

    # Source transaction identification
    transaction_id = models.CharField(
        max_length=100,
        db_index=True,
    )

    transaction_date = models.DateField(
        db_index=True,
    )

    # Organisational information
    department = models.CharField(
        max_length=150,
        db_index=True,
    )

    expense_category = models.CharField(
        max_length=150,
        db_index=True,
    )

    vendor_supplier = models.CharField(
        max_length=255,
        db_index=True,
    )

    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    # Financial information
    transaction_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )

    budget_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
    )

    # Transaction controls
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default="bank_transfer",
    )

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    transaction_description = models.TextField(
        blank=True,
        null=True,
    )

    # Data provenance
    source_file = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    imported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="imported_financial_records",
    )

    imported_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-transaction_date", "-imported_at"]
        verbose_name = "Financial Data"
        verbose_name_plural = "Financial Data"

        indexes = [
            models.Index(
                fields=["engagement", "transaction_date"],
                name="financial_eng_date_idx",
            ),
            models.Index(
                fields=["department"],
                name="financial_department_idx",
            ),
            models.Index(
                fields=["expense_category"],
                name="financial_category_idx",
            ),
            models.Index(
                fields=["vendor_supplier"],
                name="financial_vendor_idx",
            ),
            models.Index(
                fields=["approval_status"],
                name="financial_approval_idx",
            ),
            models.Index(
                fields=["payment_status"],
                name="financial_payment_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.transaction_id} - "
            f"{self.vendor_supplier} - "
            f"{self.transaction_amount}"
        )