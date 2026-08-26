from datetime import date

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.engagements.models import Engagement
from apps.risk.models import Risk
from apps.risk.views import RiskViewSet
from apps.users.models import User


class RiskRBACAPITestCase(TestCase):
    """
    Regression tests for IAPS Risk module RBAC.

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

        # ---------------------------------------------------------
        # Users
        # ---------------------------------------------------------

        cls.admin = User.objects.create_user(
            username="risk_test_admin",
            email="risk_test_admin@example.com",
            password="TestPass123!",
            role="admin",
        )

        cls.supervisor = User.objects.create_user(
            username="risk_test_supervisor",
            email="risk_test_supervisor@example.com",
            password="TestPass123!",
            role="supervisor",
        )

        cls.auditor = User.objects.create_user(
            username="risk_test_auditor",
            email="risk_test_auditor@example.com",
            password="TestPass123!",
            role="auditor",
        )

        cls.finance_manager = User.objects.create_user(
            username="risk_test_finance",
            email="risk_test_finance@example.com",
            password="TestPass123!",
            role="finance_manager",
        )

        # ---------------------------------------------------------
        # Engagement
        # ---------------------------------------------------------

        cls.engagement = Engagement.objects.create(
            engagement_code="RBAC-TEST-2026-001",
            title="Risk RBAC Test Engagement",
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

        # ---------------------------------------------------------
        # Risk record
        # ---------------------------------------------------------

        cls.risk = Risk.objects.create(
            engagement=cls.engagement,
            assessed_by=cls.auditor,
            risk_area="RBAC Test Risk",
            assertion="Accuracy",
            risk_description="Risk created for RBAC regression testing.",
            risk_factors="Automated test.",
            inherent_risk_score=50,
            control_risk_score=40,
            fraud_risk=False,
            fraud_risk_score=0,
            anomaly_detected=False,
            anomaly_score=0,
            status="assessed",
        )

        cls.factory = APIRequestFactory()

    # =========================================================
    # Helper
    # =========================================================

    @classmethod
    def request(cls, method, user, pk=None, data=None):

        path = "/api/risk/"

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

    def test_admin_can_view_risks(self):

        request = self.request(
            "GET",
            self.admin,
        )

        view = RiskViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_supervisor_can_view_risks(self):

        request = self.request(
            "GET",
            self.supervisor,
        )

        view = RiskViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_auditor_can_view_risks(self):

        request = self.request(
            "GET",
            self.auditor,
        )

        view = RiskViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_finance_manager_cannot_view_risks(self):

        request = self.request(
            "GET",
            self.finance_manager,
        )

        view = RiskViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            403,
        )
    # =========================================================
    # CREATE
    # =========================================================

    def create_payload(self, risk_area):

        return {
            "engagement": str(self.engagement.id),
            "risk_area": risk_area,
            "assertion": "Accuracy",
            "risk_description": "Automated RBAC creation test.",
            "risk_factors": "Test risk factor.",
            "inherent_risk_score": 50,
            "control_risk_score": 40,
            "fraud_risk": False,
            "fraud_risk_score": 0,
            "anomaly_detected": False,
            "anomaly_score": 0,
            "status": "assessed",
        }

    def test_admin_can_create_risk(self):

        request = self.request(
            "POST",
            self.admin,
            data=self.create_payload(
                "Admin Create Test",
            ),
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

    def test_supervisor_can_create_risk(self):

        request = self.request(
            "POST",
            self.supervisor,
            data=self.create_payload(
                "Supervisor Create Test",
            ),
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

    def test_auditor_can_create_risk(self):

        request = self.request(
            "POST",
            self.auditor,
            data=self.create_payload(
                "Auditor Create Test",
            ),
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

    def test_finance_manager_cannot_create_risk(self):

        request = self.request(
            "POST",
            self.finance_manager,
            data=self.create_payload(
                "Finance Create Test",
            ),
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            403,
        )
    # =========================================================
    # PATCH
    # =========================================================

    def test_admin_can_update_risk(self):

        request = self.request(
            "PATCH",
            self.admin,
            pk=self.risk.id,
            data={"status": "reviewed"},
        )

        view = RiskViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.risk.id,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_supervisor_can_update_risk(self):

        request = self.request(
            "PATCH",
            self.supervisor,
            pk=self.risk.id,
            data={"status": "reviewed"},
        )

        view = RiskViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.risk.id,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_auditor_cannot_update_risk(self):

        original_status = self.risk.status

        request = self.request(
            "PATCH",
            self.auditor,
            pk=self.risk.id,
            data={"status": "reviewed"},
        )

        view = RiskViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.risk.id,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.risk.refresh_from_db()

        self.assertEqual(
            self.risk.status,
            original_status,
        )

    def test_finance_manager_cannot_update_risk(self):

        request = self.request(
            "PATCH",
            self.finance_manager,
            pk=self.risk.id,
            data={"status": "reviewed"},
        )

        view = RiskViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=self.risk.id,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # =========================================================
    # DELETE
    # =========================================================

    def test_admin_can_delete_risk(self):

        risk = Risk.objects.create(
            engagement=self.engagement,
            assessed_by=self.auditor,
            risk_area="Admin Delete Test",
            assertion="Accuracy",
            risk_description="Admin deletion test.",
            status="assessed",
        )

        request = self.request(
            "DELETE",
            self.admin,
            pk=risk.id,
        )

        view = RiskViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=risk.id,
        )

        self.assertEqual(
            response.status_code,
            204,
        )

        self.assertFalse(
            Risk.objects.filter(pk=risk.id).exists()
        )

    def test_supervisor_can_delete_risk(self):

        risk = Risk.objects.create(
            engagement=self.engagement,
            assessed_by=self.auditor,
            risk_area="Supervisor Delete Test",
            assertion="Accuracy",
            risk_description="Supervisor deletion test.",
            status="assessed",
        )

        request = self.request(
            "DELETE",
            self.supervisor,
            pk=risk.id,
        )

        view = RiskViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=risk.id,
        )

        self.assertEqual(
            response.status_code,
            204,
        )

        self.assertFalse(
            Risk.objects.filter(pk=risk.id).exists()
        )

    def test_auditor_cannot_delete_risk(self):

        risk_id = self.risk.id

        request = self.request(
            "DELETE",
            self.auditor,
            pk=risk_id,
        )

        view = RiskViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=risk_id,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertTrue(
            Risk.objects.filter(pk=risk_id).exists()
        )

    def test_finance_manager_cannot_delete_risk(self):

        risk_id = self.risk.id

        request = self.request(
            "DELETE",
            self.finance_manager,
            pk=risk_id,
        )

        view = RiskViewSet.as_view({
            "delete": "destroy",
        })

        response = view(
            request,
            pk=risk_id,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertTrue(
            Risk.objects.filter(pk=risk_id).exists()
        )

    # =========================================================
    # Risk Assessment - Workflow Status RBAC
    # =========================================================

    def test_auditor_can_create_draft_risk(self):

        payload = self.create_payload(
            "Auditor Draft Workflow Test",
        )

        payload["status"] = "draft"

        request = self.request(
            "POST",
            self.auditor,
            data=payload,
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            response.data["status"],
            "draft",
        )


    def test_auditor_can_create_assessed_risk(self):

        payload = self.create_payload(
            "Auditor Assessed Workflow Test",
        )

        payload["status"] = "assessed"

        request = self.request(
            "POST",
            self.auditor,
            data=payload,
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            response.data["status"],
            "assessed",
        )


    def test_auditor_cannot_create_reviewed_risk(self):

        payload = self.create_payload(
            "Auditor Reviewed Workflow Test",
        )

        payload["status"] = "reviewed"

        request = self.request(
            "POST",
            self.auditor,
            data=payload,
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertIn(
            "status",
            response.data,
        )


    def test_auditor_cannot_create_approved_risk(self):

        payload = self.create_payload(
            "Auditor Approved Workflow Test",
        )

        payload["status"] = "approved"

        request = self.request(
            "POST",
            self.auditor,
            data=payload,
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertIn(
            "status",
            response.data,
        )


    def test_supervisor_can_create_reviewed_risk(self):

        payload = self.create_payload(
            "Supervisor Reviewed Workflow Test",
        )

        payload["status"] = "reviewed"

        request = self.request(
            "POST",
            self.supervisor,
            data=payload,
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            response.data["status"],
            "reviewed",
        )


    def test_supervisor_can_create_approved_risk(self):

        payload = self.create_payload(
            "Supervisor Approved Workflow Test",
        )

        payload["status"] = "approved"

        request = self.request(
            "POST",
            self.supervisor,
            data=payload,
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            response.data["status"],
            "approved",
        )


    def test_admin_can_create_approved_risk(self):

        payload = self.create_payload(
            "Admin Approved Workflow Test",
        )

        payload["status"] = "approved"

        request = self.request(
            "POST",
            self.admin,
            data=payload,
        )

        view = RiskViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            response.data["status"],
            "approved",
        )

    def test_auditor_cannot_change_existing_risk_to_reviewed(self):

        risk = Risk.objects.create(
            engagement=self.engagement,
            assessed_by=self.auditor,
            risk_area="Auditor Workflow Transition Test",
            assertion="Accuracy",
            risk_description="Testing auditor workflow transition.",
            risk_factors="Test risk factor.",
            inherent_risk_score=50,
            control_risk_score=40,
            fraud_risk=False,
            fraud_risk_score=0,
            anomaly_detected=False,
            anomaly_score=0,
            status="draft",
        )

        request = self.request(
            "PATCH",
            self.auditor,
            pk=risk.id,
            data={
                "status": "reviewed",
            },
        )

        view = RiskViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=risk.id,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        risk.refresh_from_db()

        self.assertEqual(
            risk.status,
            "draft",
        )


    def test_auditor_cannot_change_existing_risk_to_approved(self):

        risk = Risk.objects.create(
            engagement=self.engagement,
            assessed_by=self.auditor,
            risk_area="Auditor Approval Transition Test",
            assertion="Accuracy",
            risk_description="Testing auditor approval transition.",
            risk_factors="Test risk factor.",
            inherent_risk_score=50,
            control_risk_score=40,
            fraud_risk=False,
            fraud_risk_score=0,
            anomaly_detected=False,
            anomaly_score=0,
            status="draft",
        )

        request = self.request(
            "PATCH",
            self.auditor,
            pk=risk.id,
            data={
                "status": "approved",
            },
        )

        view = RiskViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(
            request,
            pk=risk.id,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        risk.refresh_from_db()

        self.assertEqual(
            risk.status,
            "draft",
        )