"""
IAPS API URL routing.
"""

from rest_framework.routers import DefaultRouter

from apps.engagements.views import EngagementViewSet
from apps.financial.views import FinancialDataViewSet
from apps.risk.views import RiskViewSet

from apps.planning.views import (
    AuditPlanViewSet,
    AuditProcedureViewSet,
    AIRecommendationViewSet,
)

from apps.documents.views import DocumentViewSet
from apps.audit_trail.views import AuditLogViewSet


router = DefaultRouter()

router.register(
    r"engagements",
    EngagementViewSet,
    basename="engagement",
)

router.register(
    r"financial",
    FinancialDataViewSet,
    basename="financial",
)

router.register(
    r"risks",
    RiskViewSet,
    basename="risk",
)

router.register(
    r"planning/plans",
    AuditPlanViewSet,
    basename="audit-plan",
)

router.register(
    r"planning/procedures",
    AuditProcedureViewSet,
    basename="audit-procedure",
)

router.register(
    r"planning/recommendations",
    AIRecommendationViewSet,
    basename="ai-recommendation",
)

router.register(
    r"documents",
    DocumentViewSet,
    basename="document",
)

router.register(
    r"audit-logs",
    AuditLogViewSet,
    basename="audit-log",
)


urlpatterns = router.urls