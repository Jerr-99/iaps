"""
API views for IAPS audit planning.
"""

from rest_framework import viewsets

from apps.planning.models import (
    AIRecommendation,
    AuditPlan,
    AuditProcedure,
)

from apps.planning.serializers import (
    AIRecommendationSerializer,
    AuditPlanSerializer,
    AuditProcedureSerializer,
)
from apps.planning.permissions import PlanningPermission


class AuditPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint for audit plans.
    """

    queryset = AuditPlan.objects.select_related(
        "engagement",
        "prepared_by",
        "reviewed_by",
    ).all()

    serializer_class = AuditPlanSerializer

    permission_classes = [
        PlanningPermission,
    ]

    def perform_create(self, serializer):
        """
        Automatically assign the authenticated user
        as the person preparing the audit plan.
        """

        serializer.save(
            prepared_by=self.request.user,
        )


class AuditProcedureViewSet(viewsets.ModelViewSet):
    """
    API endpoint for audit procedures.
    """

    queryset = AuditProcedure.objects.select_related(
        "audit_plan",
        "risk",
        "assigned_to",
    ).all()

    serializer_class = AuditProcedureSerializer

    permission_classes = [
        PlanningPermission,
    ]


class AIRecommendationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for AI-assisted audit recommendations.

    Recommendations are generated/stored by the system but
    remain subject to human auditor review.
    """

    queryset = AIRecommendation.objects.select_related(
        "audit_plan",
        "risk",
        "reviewed_by",
    ).all()

    serializer_class = AIRecommendationSerializer

    permission_classes = [
        PlanningPermission,
    ]