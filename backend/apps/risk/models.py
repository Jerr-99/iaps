"""
Risk assessment models for IAPS
Intelligent Audit Planning System for NCDC
"""

from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Risk(models.Model):
    """
    Stores the audit risk assessment for a specific area/account
    within an audit engagement.

    IAPS uses:
        ROMM = Inherent Risk × Control Risk

    Risk assessment is used to determine audit focus and
    support audit planning decisions.
    """

    RISK_LEVEL_CHOICES = (
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("assessed", "Assessed"),
        ("reviewed", "Reviewed"),
        ("approved", "Approved"),
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    engagement = models.ForeignKey(
        "engagements.Engagement",
        on_delete=models.CASCADE,
        related_name="risks",
    )

    assessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="risk_assessments",
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_risk_assessments",
    )

    # ------------------------------------------------------------------
    # Risk identification
    # ------------------------------------------------------------------

    risk_area = models.CharField(
        max_length=150,
        help_text="Financial statement account, business area, or audit area being assessed.",
    )

    assertion = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Relevant audit assertion, such as existence, completeness, accuracy, or valuation.",
    )

    risk_description = models.TextField(
        help_text="Description of the identified risk.",
    )

    risk_factors = models.TextField(
        blank=True,
        null=True,
        help_text="Factors contributing to the identified risk.",
    )

    # ------------------------------------------------------------------
    # Inherent Risk
    # ------------------------------------------------------------------

    inherent_risk_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("100")),
        ],
        default=Decimal("0"),
        help_text="Inherent risk score from 0 to 100.",
    )

    inherent_risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default="low",
    )

    # ------------------------------------------------------------------
    # Control Risk
    # ------------------------------------------------------------------

    control_risk_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("100")),
        ],
        default=Decimal("0"),
        help_text="Control risk score from 0 to 100.",
    )

    control_risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default="low",
    )

    # ------------------------------------------------------------------
    # ROMM
    # ------------------------------------------------------------------

    romm_score = models.DecimalField(
        max_digits=7,
        decimal_places=4,
        default=Decimal("0"),
        help_text="Risk of Material Misstatement calculated from inherent and control risk.",
    )

    romm_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default="low",
    )

    # ------------------------------------------------------------------
    # Additional risk indicators
    # ------------------------------------------------------------------

    fraud_risk = models.BooleanField(
        default=False,
        help_text="Indicates whether fraud risk factors have been identified.",
    )

    fraud_risk_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0"),
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("100")),
        ],
    )

    anomaly_detected = models.BooleanField(
        default=False,
        help_text="Indicates whether financial-data analysis identified an anomaly.",
    )

    anomaly_score = models.DecimalField(
        max_digits=7,
        decimal_places=4,
        default=Decimal("0"),
    )

    # ------------------------------------------------------------------
    # Auditor assessment
    # ------------------------------------------------------------------

    auditor_assessment = models.TextField(
        blank=True,
        null=True,
        help_text="Professional assessment and explanation by the auditor.",
    )

    recommended_response = models.TextField(
        blank=True,
        null=True,
        help_text="Suggested audit response to the identified risk.",
    )

    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    assessed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        ordering = ["-romm_score", "-created_at"]

        verbose_name = "Risk Assessment"
        verbose_name_plural = "Risk Assessments"

        indexes = [
            models.Index(
                fields=["engagement"],
                name="risk_engagement_idx",
            ),
            models.Index(
                fields=["risk_area"],
                name="risk_area_idx",
            ),
            models.Index(
                fields=["romm_level"],
                name="risk_romm_level_idx",
            ),
            models.Index(
                fields=["status"],
                name="risk_status_idx",
            ),
            models.Index(
                fields=["fraud_risk"],
                name="risk_fraud_idx",
            ),
        ]

    def __str__(self):
        return f"{self.risk_area} - {self.get_romm_level_display()}"

    # ------------------------------------------------------------------
    # Risk calculation
    # ------------------------------------------------------------------

    def calculate_romm(self):
        """
        Calculate Risk of Material Misstatement.

        Conceptually:

            ROMM = Inherent Risk × Control Risk

        Scores are stored as percentages from 0 to 100.

        Therefore:

            80 × 70 / 100 = 56

        The resulting ROMM score remains on a 0–100 scale.
        """

        inherent = Decimal(self.inherent_risk_score or 0)
        control = Decimal(self.control_risk_score or 0)

        self.romm_score = (
            inherent * control / Decimal("100")
        ).quantize(Decimal("0.0001"))

        self.romm_level = self._get_risk_level(
            self.romm_score
        )

        return self.romm_score

    # ------------------------------------------------------------------
    # Risk-level calculation
    # ------------------------------------------------------------------

    @staticmethod
    def _get_risk_level(score):
        """
        Convert a numerical risk score into a risk category.
        """

        score = Decimal(score or 0)

        if score >= Decimal("75"):
            return "critical"

        if score >= Decimal("50"):
            return "high"

        if score >= Decimal("25"):
            return "moderate"

        return "low"

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):
        """
        Automatically calculate ROMM before saving.
        """

        self.inherent_risk_level = self._get_risk_level(
            self.inherent_risk_score
        )

        self.control_risk_level = self._get_risk_level(
            self.control_risk_score
        )

        self.calculate_romm()

        super().save(*args, **kwargs)