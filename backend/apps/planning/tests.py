from datetime import date
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.engagements.models import Engagement
from apps.planning.models import (
    AIRecommendation,
    AuditPlan,
    AuditProcedure,
)
from apps.planning.views import (
    AIRecommendationViewSet,
    AuditPlanViewSet,
    AuditProcedureViewSet,
)
from apps.users.models import User


class PlanningRBACAPITestCase(TestCase):
    """
    Regression tests for IAPS Planning module RBAC.

    RBAC matrix:

        Administrator:
            GET / POST / PATCH / DELETE

        Audit Supervisor:
            GET / POST / PATCH / DELETE

        Auditor:
            GET / POST / PATCH
            DELETE denied

        Finance Manager:
            No access
    """

    @classmethod
    def setUpTestData(cls):

        # ---------------------------------------------------------
        # Users
        # ---------------------------------------------------------

        cls.admin = User.objects.create_user(
            username="planning_test_admin",
            email="planning_test_admin@example.com",
            password="TestPass123!",
            role="admin",
        )

        cls.supervisor = User.objects.create_user(
            username="planning_test_supervisor",
            email="planning_test_supervisor@example.com",
            password="TestPass123!",
            role="supervisor",
        )

        cls.auditor = User.objects.create_user(
            username="planning_test_auditor",
            email="planning_test_auditor@example.com",
            password="TestPass123!",
            role="auditor",
        )

        cls.finance_manager = User.objects.create_user(
            username="planning_test_finance",
            email="planning_test_finance@example.com",
            password="TestPass123!",
            role="finance_manager",
        )

        # ---------------------------------------------------------
        # Engagement
        # ---------------------------------------------------------

        cls.engagement = Engagement.objects.create(
            engagement_code="PLN-RBAC-2026-001",
            title="Planning RBAC Test Engagement",
            description="Automated Planning RBAC regression test.",
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
        # Audit Plan
        # ---------------------------------------------------------

        cls.audit_plan = AuditPlan.objects.create(
            engagement=cls.engagement,
            title="Planning RBAC Test Plan",
            objectives="Test Planning module RBAC.",
            scope="Financial planning controls.",
            status="draft",
            prepared_by=cls.auditor,
        )

        # ---------------------------------------------------------
        # Audit Procedure
        # ---------------------------------------------------------

        cls.procedure = AuditProcedure.objects.create(
            audit_plan=cls.audit_plan,
            name="Test Audit Procedure",
            description="Procedure created for RBAC testing.",
            procedure_type="inspection",
            objective="Verify planning permissions.",
            status="planned",
            priority=1,
            assigned_to=cls.auditor,
        )

        # ---------------------------------------------------------
        # AI Recommendation
        # ---------------------------------------------------------

        cls.recommendation = AIRecommendation.objects.create(
            audit_plan=cls.audit_plan,
            recommendation_type="Risk Response",
            recommendation="Increase substantive testing.",
            rationale="High planning risk.",
            confidence_score=Decimal("85.00"),
            model_name="IAPS-Test-Model",
            status="generated",
        )

        cls.factory = APIRequestFactory()

    # =========================================================
    # Helper
    # =========================================================

    @classmethod
    def request(cls, method, user, pk=None, data=None):

        path = "/api/planning/"

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
    # Audit Plan - GET
    # =========================================================

    def test_admin_can_view_audit_plans(self):

        request = self.request("GET", self.admin)

        view = AuditPlanViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_supervisor_can_view_audit_plans(self):

        request = self.request("GET", self.supervisor)

        view = AuditPlanViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_auditor_can_view_audit_plans(self):

        request = self.request("GET", self.auditor)

        view = AuditPlanViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_finance_manager_cannot_view_audit_plans(self):

        request = self.request("GET", self.finance_manager)

        view = AuditPlanViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # Audit Plan - DELETE
    # =========================================================

    def test_admin_can_delete_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Admin Delete Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "DELETE",
            self.admin,
            pk=plan.id,
        )

        view = AuditPlanViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 204)

    def test_supervisor_can_delete_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Supervisor Delete Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "DELETE",
            self.supervisor,
            pk=plan.id,
        )

        view = AuditPlanViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 204)

    def test_auditor_cannot_delete_audit_plan(self):

        request = self.request(
            "DELETE",
            self.auditor,
            pk=self.audit_plan.id,
        )

        view = AuditPlanViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    def test_finance_manager_cannot_delete_audit_plan(self):

        request = self.request(
            "DELETE",
            self.finance_manager,
            pk=self.audit_plan.id,
        )

        view = AuditPlanViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # Audit Procedure - GET
    # =========================================================

    def test_auditor_can_view_procedures(self):

        request = self.request("GET", self.auditor)

        view = AuditProcedureViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_finance_manager_cannot_view_procedures(self):

        request = self.request("GET", self.finance_manager)

        view = AuditProcedureViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # Audit Procedure - DELETE
    # =========================================================

    def test_admin_can_delete_procedure(self):

        procedure = AuditProcedure.objects.create(
            audit_plan=self.audit_plan,
            name="Admin Delete Procedure",
            description="Delete test.",
            procedure_type="inspection",
            assigned_to=self.auditor,
        )

        request = self.request(
            "DELETE",
            self.admin,
            pk=procedure.id,
        )

        view = AuditProcedureViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request, pk=procedure.id)

        self.assertEqual(response.status_code, 204)

    def test_auditor_cannot_delete_procedure(self):

        request = self.request(
            "DELETE",
            self.auditor,
            pk=self.procedure.id,
        )

        view = AuditProcedureViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # AI Recommendation - GET
    # =========================================================

    def test_admin_can_view_recommendations(self):

        request = self.request("GET", self.admin)

        view = AIRecommendationViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_supervisor_can_view_recommendations(self):

        request = self.request("GET", self.supervisor)

        view = AIRecommendationViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_auditor_can_view_recommendations(self):

        request = self.request("GET", self.auditor)

        view = AIRecommendationViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_finance_manager_cannot_view_recommendations(self):

        request = self.request("GET", self.finance_manager)

        view = AIRecommendationViewSet.as_view({
            "get": "list",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # AI Recommendation - DELETE
    # =========================================================

    def test_admin_can_delete_recommendation(self):

        recommendation = AIRecommendation.objects.create(
            audit_plan=self.audit_plan,
            recommendation_type="Delete Test",
            recommendation="Test recommendation.",
            confidence_score=Decimal("70.00"),
        )

        request = self.request(
            "DELETE",
            self.admin,
            pk=recommendation.id,
        )

        view = AIRecommendationViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request, pk=recommendation.id)

        self.assertEqual(response.status_code, 204)

    def test_supervisor_can_delete_recommendation(self):

        recommendation = AIRecommendation.objects.create(
            audit_plan=self.audit_plan,
            recommendation_type="Supervisor Delete Test",
            recommendation="Test recommendation.",
            confidence_score=Decimal("70.00"),
        )

        request = self.request(
            "DELETE",
            self.supervisor,
            pk=recommendation.id,
        )

        view = AIRecommendationViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request, pk=recommendation.id)

        self.assertEqual(response.status_code, 204)

    def test_auditor_cannot_delete_recommendation(self):

        request = self.request(
            "DELETE",
            self.auditor,
            pk=self.recommendation.id,
        )

        view = AIRecommendationViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    def test_finance_manager_cannot_delete_recommendation(self):

        request = self.request(
            "DELETE",
            self.finance_manager,
            pk=self.recommendation.id,
        )

        view = AIRecommendationViewSet.as_view({
            "delete": "destroy",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)

    
    # =========================================================
    # Audit Plan - Approval Workflow
    # =========================================================

    def test_admin_can_approve_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Admin Approval Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.admin,
            pk=plan.id,
            data={"status": "approved"},
        )

        view = AuditPlanViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "approved")

    def test_supervisor_can_approve_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Supervisor Approval Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.supervisor,
            pk=plan.id,
            data={"status": "approved"},
        )

        view = AuditPlanViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "approved")

    def test_auditor_cannot_approve_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Auditor Approval Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.auditor,
            pk=plan.id,
            data={"status": "approved"},
        )

        view = AuditPlanViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 400)
        self.assertIn("status", response.data)

    def test_auditor_cannot_complete_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Auditor Completion Test",
            status="approved",
            prepared_by=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.auditor,
            pk=plan.id,
            data={"status": "completed"},
        )

        view = AuditPlanViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 400)
        self.assertIn("status", response.data)

    def test_finance_manager_cannot_approve_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Finance Approval Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.finance_manager,
            pk=plan.id,
            data={"status": "approved"},
        )

        view = AuditPlanViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 403)

        # =========================================================
    # Audit Plan - Normal Update
    # =========================================================

    def test_auditor_can_update_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Auditor Update Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.auditor,
            pk=plan.id,
            data={"title": "Auditor Updated Plan"},
        )

        view = AuditPlanViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["title"],
            "Auditor Updated Plan",
        )

    def test_finance_manager_cannot_update_audit_plan(self):

        plan = AuditPlan.objects.create(
            engagement=self.engagement,
            title="Finance Update Test",
            status="draft",
            prepared_by=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.finance_manager,
            pk=plan.id,
            data={"title": "Unauthorized Update"},
        )

        view = AuditPlanViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=plan.id)

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # Audit Plan - CREATE
    # =========================================================

    def test_auditor_can_create_audit_plan(self):

        request = self.request(
            "POST",
            self.auditor,
            data={
                "engagement": self.engagement.id,
                "title": "Auditor Created Plan",
                "objectives": "Test auditor creation.",
                "scope": "Planning controls.",
                "status": "draft",
            },
        )

        view = AuditPlanViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["title"],
            "Auditor Created Plan",
        )
        self.assertEqual(
            response.data["prepared_by"],
            self.auditor.id,
        )

    def test_finance_manager_cannot_create_audit_plan(self):

        request = self.request(
            "POST",
            self.finance_manager,
            data={
                "engagement": self.engagement.id,
                "title": "Finance Created Plan",
                "objectives": "Unauthorized creation.",
                "scope": "Planning controls.",
                "status": "draft",
            },
        )

        view = AuditPlanViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)
    # =========================================================
    # Audit Procedure - CREATE / UPDATE
    # =========================================================

    def test_auditor_can_create_audit_procedure(self):

        request = self.request(
            "POST",
            self.auditor,
            data={
                "audit_plan": self.audit_plan.id,
                "name": "Auditor Created Procedure",
                "description": "Procedure created by auditor.",
                "procedure_type": "inspection",
                "objective": "Verify planning controls.",
                "status": "planned",
                "priority": 1,
                "assigned_to": self.auditor.id,
            },
        )

        view = AuditProcedureViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["name"],
            "Auditor Created Procedure",
        )


    def test_auditor_can_update_audit_procedure(self):

        procedure = AuditProcedure.objects.create(
            audit_plan=self.audit_plan,
            name="Auditor Procedure Update Test",
            description="Original procedure.",
            procedure_type="inspection",
            objective="Original objective.",
            status="planned",
            priority=1,
            assigned_to=self.auditor,
        )

        request = self.request(
            "PATCH",
            self.auditor,
            pk=procedure.id,
            data={
                "name": "Auditor Updated Procedure",
            },
        )

        view = AuditProcedureViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=procedure.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["name"],
            "Auditor Updated Procedure",
        )


    def test_finance_manager_cannot_create_audit_procedure(self):

        request = self.request(
            "POST",
            self.finance_manager,
            data={
                "audit_plan": self.audit_plan.id,
                "name": "Finance Created Procedure",
                "description": "Unauthorized procedure.",
                "procedure_type": "inspection",
                "objective": "Unauthorized objective.",
                "status": "planned",
                "priority": 1,
                "assigned_to": self.auditor.id,
            },
        )

        view = AuditProcedureViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)


    # =========================================================
    # AI Recommendation - CREATE / UPDATE
    # =========================================================

    def test_auditor_can_create_ai_recommendation(self):

        request = self.request(
            "POST",
            self.auditor,
            data={
                "audit_plan": self.audit_plan.id,
                "recommendation_type": "Risk Response",
                "recommendation": "Increase substantive testing.",
                "rationale": "Elevated planning risk.",
                "confidence_score": 85,
                "model_name": "IAPS-Test-Model",
                "status": "generated",
            },
        )

        view = AIRecommendationViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["recommendation"],
            "Increase substantive testing.",
        )
        self.assertEqual(
            Decimal(str(response.data["confidence_score"])),
            Decimal("85.00"),
        )


    def test_auditor_can_update_ai_recommendation(self):

        recommendation = AIRecommendation.objects.create(
            audit_plan=self.audit_plan,
            recommendation_type="Update Test",
            recommendation="Original recommendation.",
            rationale="Original rationale.",
            confidence_score=Decimal("75.00"),
            model_name="IAPS-Test-Model",
            status="generated",
        )

        request = self.request(
            "PATCH",
            self.auditor,
            pk=recommendation.id,
            data={
                "recommendation": "Auditor Updated Recommendation",
            },
        )

        view = AIRecommendationViewSet.as_view({
            "patch": "partial_update",
        })

        response = view(request, pk=recommendation.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["recommendation"],
            "Auditor Updated Recommendation",
        )


    def test_finance_manager_cannot_create_ai_recommendation(self):

        request = self.request(
            "POST",
            self.finance_manager,
            data={
                "audit_plan": self.audit_plan.id,
                "recommendation_type": "Unauthorized",
                "recommendation": "Finance recommendation.",
                "rationale": "Unauthorized creation.",
                "confidence_score": 80,
                "model_name": "IAPS-Test-Model",
                "status": "generated",
            },
        )

        view = AIRecommendationViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 403)


    # =========================================================
    # AI Recommendation - Confidence Validation
    # =========================================================

    def test_ai_confidence_above_100_rejected(self):

        request = self.request(
            "POST",
            self.auditor,
            data={
                "audit_plan": self.audit_plan.id,
                "recommendation_type": "Confidence Test",
                "recommendation": "Invalid high confidence.",
                "rationale": "Testing upper boundary.",
                "confidence_score": 101,
                "model_name": "IAPS-Test-Model",
                "status": "generated",
            },
        )

        view = AIRecommendationViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("confidence_score", response.data)


    def test_ai_confidence_below_0_rejected(self):

        request = self.request(
            "POST",
            self.auditor,
            data={
                "audit_plan": self.audit_plan.id,
                "recommendation_type": "Confidence Test",
                "recommendation": "Invalid low confidence.",
                "rationale": "Testing lower boundary.",
                "confidence_score": -1,
                "model_name": "IAPS-Test-Model",
                "status": "generated",
            },
        )

        view = AIRecommendationViewSet.as_view({
            "post": "create",
        })

        response = view(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("confidence_score", response.data)

