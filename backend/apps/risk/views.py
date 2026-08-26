from rest_framework import viewsets

from apps.audit_trail.services import create_audit_log
from apps.risk.models import Risk
from apps.risk.permissions import RiskPermission
from apps.risk.serializers import RiskSerializer


class RiskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for IAPS risk assessments.

    RBAC is enforced by RiskPermission.

    Workflow status restrictions are enforced by RiskSerializer.
    """

    queryset = Risk.objects.select_related(
        "engagement",
        "assessed_by",
        "reviewed_by",
    ).all()

    serializer_class = RiskSerializer

    permission_classes = [
        RiskPermission,
    ]

    def perform_create(self, serializer):
        """
        Create a risk assessment.

        The authenticated user is automatically assigned
        as the assessor.

        A corresponding audit-trail entry is created.
        """

        risk = serializer.save(
            assessed_by=self.request.user,
        )

        create_audit_log(
            user=self.request.user,
            action="create",
            module="risk",
            object_type="Risk",
            object_id=risk.id,
            description=(
                f"Risk assessment created for "
                f"{risk.risk_area}."
            ),
            old_values={},
            new_values={
                "risk_area": risk.risk_area,
                "assertion": risk.assertion,
                "inherent_risk_score": str(
                    risk.inherent_risk_score
                ),
                "control_risk_score": str(
                    risk.control_risk_score
                ),
                "fraud_risk": risk.fraud_risk,
                "fraud_risk_score": (
                    str(risk.fraud_risk_score)
                    if risk.fraud_risk_score is not None
                    else None
                ),
                "anomaly_detected": risk.anomaly_detected,
                "anomaly_score": (
                    str(risk.anomaly_score)
                    if risk.anomaly_score is not None
                    else None
                ),
                "status": risk.status,
            },
            ip_address=self.request.META.get(
                "REMOTE_ADDR"
            ),
            user_agent=self.request.META.get(
                "HTTP_USER_AGENT"
            ),
        )