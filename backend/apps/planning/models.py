"""
Audit planning models for IAPS.

The planning module represents the Planning Phase of the
Intelligent Audit Planning System (IAPS).

It links:
    Engagements
        ↓
    Identified Risks
        ↓
    Audit Procedures
        ↓
    AI-assisted Recommendations
"""

from django.conf import settings
from django.db import models


class AuditPlan(models.Model):
    """
    Audit plan for a specific audit engagement.

    An engagement can have one or more planning records as the
    audit develops, but normally the active plan represents the
    approved planning phase.
    """

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("in_progress", "In Progress"),
        ("review", "Under Review"),
        ("approved", "Approved"),
        ("completed", "Completed"),
    )

    engagement = models.ForeignKey(
        "engagements.Engagement",
        on_delete=models.CASCADE,
        related_name="audit_plans",
    )

    title = models.CharField(max_length=255)

    objectives = models.TextField(
        blank=True,
        null=True,
        help_text="Objectives established for the audit."
    )

    scope = models.TextField(
        blank=True,
        null=True,
        help_text="Scope and boundaries of the audit."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    prepared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="prepared_audit_plans",
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reviewed_audit_plans",
        blank=True,
        null=True,
    )

    planned_start_date = models.DateField(
        blank=True,
        null=True,
    )

    planned_end_date = models.DateField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Audit Plan"
        verbose_name_plural = "Audit Plans"
        indexes = [
            models.Index(fields=["engagement"]),
            models.Index(fields=["status"]),
            models.Index(fields=["prepared_by"]),
        ]

    def __str__(self):
        return self.title


class AuditProcedure(models.Model):
    """
    Individual audit procedure forming part of an audit plan.

    Procedures can be linked to identified risks so that the final
    audit plan is risk-based rather than simply a checklist.
    """

    PROCEDURE_TYPE_CHOICES = (
        ("inspection", "Inspection"),
        ("observation", "Observation"),
        ("inquiry", "Inquiry"),
        ("confirmation", "Confirmation"),
        ("recalculation", "Recalculation"),
        ("reperformance", "Reperformance"),
        ("analytical", "Analytical Procedure"),
        ("other", "Other"),
    )

    STATUS_CHOICES = (
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("deferred", "Deferred"),
    )

    audit_plan = models.ForeignKey(
        AuditPlan,
        on_delete=models.CASCADE,
        related_name="procedures",
    )

    risk = models.ForeignKey(
        "risk.Risk",
        on_delete=models.SET_NULL,
        related_name="audit_procedures",
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    procedure_type = models.CharField(
        max_length=30,
        choices=PROCEDURE_TYPE_CHOICES,
        default="other",
    )

    objective = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned",
    )

    priority = models.PositiveIntegerField(
        default=1,
        help_text="Priority of the procedure within the audit plan."
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assigned_audit_procedures",
        blank=True,
        null=True,
    )

    planned_date = models.DateField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["priority", "created_at"]
        verbose_name = "Audit Procedure"
        verbose_name_plural = "Audit Procedures"
        indexes = [
            models.Index(fields=["audit_plan"]),
            models.Index(fields=["risk"]),
            models.Index(fields=["status"]),
            models.Index(fields=["assigned_to"]),
        ]

    def __str__(self):
        return self.name


class AIRecommendation(models.Model):
    """
    AI-assisted recommendation generated during audit planning.

    This stores the recommendation and its relationship to the
    planning process. The AI does not independently approve an
    audit decision; the auditor remains responsible for reviewing
    and accepting/rejecting recommendations.
    """

    STATUS_CHOICES = (
        ("generated", "Generated"),
        ("reviewed", "Reviewed"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    audit_plan = models.ForeignKey(
        AuditPlan,
        on_delete=models.CASCADE,
        related_name="ai_recommendations",
    )

    risk = models.ForeignKey(
        "risk.Risk",
        on_delete=models.SET_NULL,
        related_name="ai_recommendations",
        blank=True,
        null=True,
    )

    recommendation_type = models.CharField(
        max_length=100,
    )

    recommendation = models.TextField()

    rationale = models.TextField(
        blank=True,
        null=True,
    )

    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="AI confidence score from 0.00 to 100.00."
    )

    model_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="generated",
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reviewed_ai_recommendations",
        blank=True,
        null=True,
    )

    reviewer_notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "AI Recommendation"
        verbose_name_plural = "AI Recommendations"
        indexes = [
            models.Index(fields=["audit_plan"]),
            models.Index(fields=["risk"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.recommendation_type} - {self.audit_plan}"