"""
Models for the IAPS Engagements app.

The Engagement model represents an audit engagement during the
planning phase of the audit process.
"""

import uuid

from django.conf import settings
from django.db import models


class Engagement(models.Model):
    """
    Represents an audit engagement managed by IAPS.

    An engagement is the central planning record to which financial
    data, risks, audit procedures, documents, recommendations and
    audit-trail records will eventually be related.
    """

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    )

    RISK_LEVEL_CHOICES = (
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    engagement_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    # NCDC organisational information
    department = models.CharField(
        max_length=150,
    )

    auditee = models.CharField(
        max_length=255,
    )

    audit_year = models.PositiveIntegerField()

    # Audit period
    start_date = models.DateField()

    end_date = models.DateField()

    # Engagement status and preliminary risk classification
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        db_index=True,
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default="moderate",
        db_index=True,
    )

    # Engagement ownership
    lead_auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="led_engagements",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_engagements",
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Audit Engagement"
        verbose_name_plural = "Audit Engagements"

        indexes = [
            models.Index(
                fields=["audit_year"],
                name="engagement_year_idx",
            ),
            models.Index(
                fields=["department"],
                name="engagement_department_idx",
            ),
            models.Index(
                fields=["status"],
                name="engagement_status_idx",
            ),
            models.Index(
                fields=["risk_level"],
                name="engagement_risk_idx",
            ),
        ]

    def __str__(self):
        return f"{self.engagement_code} - {self.title}"