from datetime import date

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.engagements.models import Engagement
from apps.engagements.views import EngagementViewSet
from apps.users.models import User


class EngagementRBACAPITestCase(TestCase):
    """
    Regression tests for IAPS Engagements module RBAC.

    RBAC matrix:

        Administrator:
            GET / POST / PATCH / DELETE

        Audit Supervisor:
            GET / POST / PATCH / DELETE

        Auditor:
            GET / POST only

        Finance Manager:
            No access
    """

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username="engagement_test_admin",
            email="engagement_test_admin@example.com",
            password="TestPass123!",
            role="admin",
        )

        cls.supervisor = User.objects.create_user(
            username="engagement_test_supervisor",
            email="engagement_test_supervisor@example.com",
            password="TestPass123!",
            role="supervisor",
        )

        cls.auditor = User.objects.create_user(
            username="engagement_test_auditor",
            email="engagement_test_auditor@example.com",
            password="TestPass123!",
            role="auditor",
        )

        cls.finance_manager = User.objects.create_user(
            username="engagement_test_finance",
            email="engagement_test_finance@example.com",
            password="TestPass123!",
            role="finance_manager",
        )

        cls.engagement = Engagement.objects.create(
            engagement_code="RBAC-ENG-TEST-001",
            title="Engagement RBAC Test",
            description="Automated RBAC regression test.",
            department="Finance",
            auditee="NCDC",
            audit_year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="planning",
            risk_level="moderate",
            lead_auditor=cls.auditor,
            created_by=cls.supervisor,
        )

        cls.factory = APIRequestFactory()

    @classmethod
    def request(cls, method, user, pk=None, data=None):

        path = "/api/engagements/"

        if pk is not None:
            path += f"{pk}/"

        request = getattr(
            cls.factory,
            method.lower(),
        )(
            path,
            data or {},
            format="json",
        )

        force_authenticate(
            request,
            user=user,
        )

        return request

    # =========================================================
    # GET
    # =========================================================

    def test_admin_can_view_engagements(self):

        request = self.request(
            "GET",
            self.admin,
        )

        view = EngagementViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_supervisor_can_view_engagements(self):

        request = self.request(
            "GET",
            self.supervisor,
        )

        view = EngagementViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_auditor_can_view_engagements(self):

        request = self.request(
            "GET",
            self.auditor,
        )

        view = EngagementViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_finance_manager_cannot_view_engagements(self):

        request = self.request(
            "GET",
            self.finance_manager,
        )

        view = EngagementViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # DELETE
    # =========================================================

    def test_admin_can_delete_engagement(self):

        engagement = Engagement.objects.create(
            engagement_code="RBAC-ENG-DELETE-ADMIN",
            title="Admin Delete Test",
            department="Finance",
            auditee="NCDC",
            audit_year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="planning",
            risk_level="moderate",
            lead_auditor=self.auditor,
            created_by=self.admin,
        )

        request = self.request(
            "DELETE",
            self.admin,
            pk=engagement.id,
        )

        view = EngagementViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=engagement.id,
        )

        self.assertEqual(response.status_code, 204)

    def test_supervisor_can_delete_engagement(self):

        engagement = Engagement.objects.create(
            engagement_code="RBAC-ENG-DELETE-SUP",
            title="Supervisor Delete Test",
            department="Finance",
            auditee="NCDC",
            audit_year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="planning",
            risk_level="moderate",
            lead_auditor=self.auditor,
            created_by=self.supervisor,
        )

        request = self.request(
            "DELETE",
            self.supervisor,
            pk=engagement.id,
        )

        view = EngagementViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=engagement.id,
        )

        self.assertEqual(response.status_code, 204)

    def test_auditor_cannot_delete_engagement(self):

        request = self.request(
            "DELETE",
            self.auditor,
            pk=self.engagement.id,
        )

        view = EngagementViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=self.engagement.id,
        )

        self.assertEqual(response.status_code, 403)

    def test_finance_manager_cannot_delete_engagement(self):

        request = self.request(
            "DELETE",
            self.finance_manager,
            pk=self.engagement.id,
        )

        view = EngagementViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=self.engagement.id,
        )

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # UPDATE
    # =========================================================

    def test_admin_can_update_engagement(self):

        request = self.request(
            "PATCH",
            self.admin,
            pk=self.engagement.id,
            data={"title": "Admin Updated Engagement"},
        )

        view = EngagementViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.engagement.id,
        )

        self.assertEqual(response.status_code, 200)

    def test_supervisor_can_update_engagement(self):

        request = self.request(
            "PATCH",
            self.supervisor,
            pk=self.engagement.id,
            data={"title": "Supervisor Updated Engagement"},
        )

        view = EngagementViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.engagement.id,
        )

        self.assertEqual(response.status_code, 200)

    def test_auditor_cannot_update_engagement(self):

        request = self.request(
            "PATCH",
            self.auditor,
            pk=self.engagement.id,
            data={"title": "Auditor Attempted Update"},
        )

        view = EngagementViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.engagement.id,
        )

        self.assertEqual(response.status_code, 403)

    def test_finance_manager_cannot_update_engagement(self):

        request = self.request(
            "PATCH",
            self.finance_manager,
            pk=self.engagement.id,
            data={"title": "Finance Attempted Update"},
        )

        view = EngagementViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.engagement.id,
        )

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # CREATE
    # =========================================================

    def create_payload(self, code):

        return {
            "engagement_code": code,
            "title": "RBAC Create Test",
            "description": "Automated creation test.",
            "department": "Finance",
            "auditee": "NCDC",
            "audit_year": 2026,
            "start_date": "2026-01-01",
            "end_date": "2026-12-31",
            "status": "draft",
            "risk_level": "moderate",
        }

    def test_admin_can_create_engagement(self):

        request = self.request(
            "POST",
            self.admin,
            data=self.create_payload(
                "RBAC-ENG-CREATE-ADMIN"
            ),
        )

        view = EngagementViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_supervisor_can_create_engagement(self):

        request = self.request(
            "POST",
            self.supervisor,
            data=self.create_payload(
                "RBAC-ENG-CREATE-SUP"
            ),
        )

        view = EngagementViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_auditor_can_create_engagement(self):

        request = self.request(
            "POST",
            self.auditor,
            data=self.create_payload(
                "RBAC-ENG-CREATE-AUD"
            ),
        )

        view = EngagementViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 201)

    def test_finance_manager_cannot_create_engagement(self):

        request = self.request(
            "POST",
            self.finance_manager,
            data=self.create_payload(
                "RBAC-ENG-CREATE-FIN"
            ),
        )

        view = EngagementViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)
