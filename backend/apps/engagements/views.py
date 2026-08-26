from rest_framework import viewsets

from apps.engagements.models import Engagement
from apps.engagements.serializers import EngagementSerializer
from apps.engagements.permissions import EngagementPermission


class EngagementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for audit engagements.

    Provides:
        GET     /api/engagements/
        POST    /api/engagements/
        GET     /api/engagements/{id}/
        PUT     /api/engagements/{id}/
        PATCH   /api/engagements/{id}/
        DELETE  /api/engagements/{id}/
    """

    queryset = Engagement.objects.select_related(
        "lead_auditor",
        "created_by",
    ).all()

    serializer_class = EngagementSerializer

    permission_classes = [
        EngagementPermission,
    ]

    def perform_create(self, serializer):
        """
        Automatically assign the authenticated user as the creator
        and lead auditor when creating an engagement.

        Also create an immutable audit-trail entry.
        """

        engagement = serializer.save(
            created_by=self.request.user,
            lead_auditor=self.request.user,
        )

        from apps.audit_trail.services import create_audit_log

        create_audit_log(
            user=self.request.user,
            action="create",
            module="engagements",
            object_type="Engagement",
            object_id=str(engagement.id),
            description=(
                f"Audit engagement created: "
                f"{engagement.engagement_code}."
            ),
            old_values={},
            new_values={
                "engagement_code": engagement.engagement_code,
                "title": engagement.title,
                "status": engagement.status,
            },
            ip_address=self.request.META.get(
                "REMOTE_ADDR"
            ),
            user_agent=self.request.META.get(
                "HTTP_USER_AGENT"
            ),
        )

    def perform_update(self, serializer):
        """
        Update an engagement and create an immutable audit-trail entry
        containing the previous and new values.
        """

        engagement = self.get_object()

        # Capture values BEFORE the update.
        old_values = {
            "engagement_code": engagement.engagement_code,
            "title": engagement.title,
            "description": engagement.description,
            "department": engagement.department,
            "auditee": engagement.auditee,
            "audit_year": engagement.audit_year,
            "start_date": str(engagement.start_date),
            "end_date": str(engagement.end_date),
            "status": engagement.status,
            "risk_level": engagement.risk_level,
        }

        # Perform the actual update.
        engagement = serializer.save()

        # Capture values AFTER the update.
        new_values = {
            "engagement_code": engagement.engagement_code,
            "title": engagement.title,
            "description": engagement.description,
            "department": engagement.department,
            "auditee": engagement.auditee,
            "audit_year": engagement.audit_year,
            "start_date": str(engagement.start_date),
            "end_date": str(engagement.end_date),
            "status": engagement.status,
            "risk_level": engagement.risk_level,
        }

        # Create immutable audit-trail record.
        from apps.audit_trail.services import create_audit_log

        create_audit_log(
            user=self.request.user,
            action="update",
            module="engagements",
            object_type="Engagement",
            object_id=str(engagement.id),
            description=(
                f"Audit engagement updated: "
                f"{engagement.engagement_code}."
            ),
            old_values=old_values,
            new_values=new_values,
            ip_address=self.request.META.get(
                "REMOTE_ADDR"
            ),
            user_agent=self.request.META.get(
                "HTTP_USER_AGENT"
            ),
        )
        
    def perform_destroy(self, instance):
        """
        Delete an engagement and create an immutable audit-trail entry
        containing the values of the engagement before deletion.
        """

        old_values = {
            "engagement_code": instance.engagement_code,
            "title": instance.title,
            "description": instance.description,
            "department": instance.department,
            "auditee": instance.auditee,
            "audit_year": instance.audit_year,
            "start_date": str(instance.start_date),
            "end_date": str(instance.end_date),
            "status": instance.status,
            "risk_level": instance.risk_level,
        }

        engagement_id = str(instance.id)
        engagement_code = instance.engagement_code

        from apps.audit_trail.services import create_audit_log

        create_audit_log(
            user=self.request.user,
            action="delete",
            module="engagements",
            object_type="Engagement",
            object_id=engagement_id,
            description=(
                f"Audit engagement deleted: "
                f"{engagement_code}."
            ),
            old_values=old_values,
            new_values={},
            ip_address=self.request.META.get(
                "REMOTE_ADDR"
            ),
            user_agent=self.request.META.get(
                "HTTP_USER_AGENT"
            ),
        )

        # Delete the engagement after the audit record is created.
        instance.delete()
    