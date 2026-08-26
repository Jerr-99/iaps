"""
Document models for IAPS.

The documents module manages documents uploaded during the
audit planning process and provides the foundation for later
document ingestion, extraction, OCR, and AI-assisted analysis.
"""

from django.conf import settings
from django.db import models


class Document(models.Model):
    """
    Document uploaded as part of an audit engagement.

    The actual document file is stored through Django's media
    storage system. Processing-related fields allow the future
    document ingestion pipeline to track extraction/OCR status.
    """

    DOCUMENT_TYPE_CHOICES = (
        ("financial_statement", "Financial Statement"),
        ("invoice", "Invoice"),
        ("receipt", "Receipt"),
        ("bank_statement", "Bank Statement"),
        ("budget", "Budget"),
        ("contract", "Contract"),
        ("audit_report", "Audit Report"),
        ("policy", "Policy"),
        ("supporting_document", "Supporting Document"),
        ("other", "Other"),
    )

    PROCESSING_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    engagement = models.ForeignKey(
        "engagements.Engagement",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_documents",
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    document_type = models.CharField(
        max_length=40,
        choices=DOCUMENT_TYPE_CHOICES,
        default="other",
    )

    file = models.FileField(
        upload_to="audit_documents/%Y/%m/",
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    file_size = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        help_text="File size in bytes."
    )

    mime_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS_CHOICES,
        default="pending",
    )

    extracted_text = models.TextField(
        blank=True,
        null=True,
    )

    processing_error = models.TextField(
        blank=True,
        null=True,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    processed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        indexes = [
            models.Index(fields=["engagement"]),
            models.Index(fields=["uploaded_by"]),
            models.Index(fields=["document_type"]),
            models.Index(fields=["processing_status"]),
            models.Index(fields=["uploaded_at"]),
        ]

    def __str__(self):
        return self.name