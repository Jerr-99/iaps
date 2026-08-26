from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.audit_trail.models import AuditLog
from apps.audit_trail.views import AuditLogViewSet
from apps.users.models import User


class AuditLogAPITestCase(TestCase):
    """
    Comprehensive regression tests for the AuditLog API.
    """

    @classmethod
    def setUpTestData(cls):

        # -------------------------------------------------
        # Create users
        # -------------------------------------------------

        cls.auditor = User.objects.create_user(
            username="test_auditor",
            email="test_auditor@example.com",
            password="testpass123",
        )

        cls.unauthorized = User.objects.create_user(
            username="test_unauthorized",
            email="test_unauthorized@example.com",
            password="testpass123",
        )

        # -------------------------------------------------
        # Assign audit-log view permission
        # -------------------------------------------------

        permission = Permission.objects.get(
            content_type__app_label="audit_trail",
            codename="view_auditlog",
        )

        cls.auditor.user_permissions.add(permission)

        # -------------------------------------------------
        # Create audit logs
        # -------------------------------------------------

        cls.log1 = AuditLog.objects.create(
            user=cls.auditor,
            action="upload",
            module="documents",
            object_type="Document",
            object_id="3",
            description="Uploaded document.",
            old_values={},
            new_values={"name": "document3.pdf"},
        )

        cls.log2 = AuditLog.objects.create(
            user=cls.auditor,
            action="upload",
            module="documents",
            object_type="Document",
            object_id="4",
            description="Uploaded document.",
            old_values={},
            new_values={"name": "document4.pdf"},
        )

        cls.log3 = AuditLog.objects.create(
            user=cls.auditor,
            action="delete",
            module="documents",
            object_type="Document",
            object_id="5",
            description="Deleted document.",
            old_values={"name": "document5.pdf"},
            new_values={},
        )

        cls.log4 = AuditLog.objects.create(
            user=cls.auditor,
            action="delete",
            module="engagements",
            object_type="Engagement",
            object_id="7",
            description="Deleted engagement.",
            old_values={},
            new_values={},
        )

        cls.factory = APIRequestFactory()

    # =====================================================
    # Helper
    # =====================================================

    def call_list(self, query="", user=None):

        if user is None:
            user = self.auditor

        request = self.factory.get(
            "/api/audit-trail/" + query
        )

        force_authenticate(
            request,
            user=user,
        )

        view = AuditLogViewSet.as_view({
            "get": "list"
        })

        return view(request)

    # =====================================================
    # TEST 1 — Authorized access
    # =====================================================

    def test_authorized_user_can_view_logs(self):

        response = self.call_list()

        self.assertEqual(
            response.status_code,
            200,
        )

    # =====================================================
    # TEST 2 — Unauthorized access
    # =====================================================

    def test_unauthorized_user_is_blocked(self):

        response = self.call_list(
            user=self.unauthorized
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # =====================================================
    # TEST 3 — Unauthenticated access
    # =====================================================

    def test_unauthenticated_user_is_blocked(self):

        request = self.factory.get(
            "/api/audit-trail/"
        )

        view = AuditLogViewSet.as_view({
            "get": "list"
        })

        response = view(request)

        self.assertEqual(
            response.status_code,
            401,
        )

    # =====================================================
    # TEST 4 — Module filter
    # =====================================================

    def test_module_filter(self):

        response = self.call_list(
            "?module=documents"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        for record in response.data["results"]:
            self.assertEqual(
                record["module"],
                "documents",
            )

    # =====================================================
    # TEST 5 — Action filter
    # =====================================================

    def test_action_filter(self):

        response = self.call_list(
            "?action=delete"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        for record in response.data["results"]:
            self.assertEqual(
                record["action"],
                "delete",
            )

    # =====================================================
    # TEST 6 — Object type filter
    # =====================================================

    def test_object_type_filter(self):

        response = self.call_list(
            "?object_type=Document"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        for record in response.data["results"]:
            self.assertEqual(
                record["object_type"],
                "Document",
            )

    # =====================================================
    # TEST 7 — Object ID filter
    # =====================================================

    def test_object_id_filter(self):

        response = self.call_list(
            "?object_id=4"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        for record in response.data["results"]:
            self.assertEqual(
                str(record["object_id"]),
                "4",
            )

    # =====================================================
    # TEST 8 — Combined filters
    # =====================================================

    def test_combined_filters(self):

        response = self.call_list(
            "?module=documents&action=upload"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        for record in response.data["results"]:

            self.assertEqual(
                record["module"],
                "documents",
            )

            self.assertEqual(
                record["action"],
                "upload",
            )

    # =====================================================
    # TEST 9 — Invalid filter
    # =====================================================

    def test_invalid_filter_returns_empty_result(self):

        response = self.call_list(
            "?module=does_not_exist"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["count"],
            0,
        )

    # =====================================================
    # TEST 10 — Retrieve authorized record
    # =====================================================

    def test_authorized_retrieve(self):

        request = self.factory.get(
            f"/api/audit-trail/{self.log1.id}/"
        )

        force_authenticate(
            request,
            user=self.auditor,
        )

        view = AuditLogViewSet.as_view({
            "get": "retrieve"
        })

        response = view(
            request,
            pk=self.log1.id,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    # =====================================================
    # TEST 11 — Retrieve unauthorized record
    # =====================================================

    def test_unauthorized_retrieve(self):

        request = self.factory.get(
            f"/api/audit-trail/{self.log1.id}/"
        )

        force_authenticate(
            request,
            user=self.unauthorized,
        )

        view = AuditLogViewSet.as_view({
            "get": "retrieve"
        })

        response = view(
            request,
            pk=self.log1.id,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # =====================================================
    # TEST 12 — Nonexistent record
    # =====================================================

    def test_nonexistent_record_returns_404(self):

        request = self.factory.get(
            "/api/audit-trail/999999/"
        )

        force_authenticate(
            request,
            user=self.auditor,
        )

        view = AuditLogViewSet.as_view({
            "get": "retrieve"
        })

        response = view(
            request,
            pk=999999,
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    # =====================================================
    # TEST 13 — Required fields
    # =====================================================

    def test_required_fields_exist(self):

        response = self.call_list()

        required_fields = [
            "id",
            "user",
            "username",
            "action",
            "module",
            "object_type",
            "object_id",
            "description",
            "old_values",
            "new_values",
            "created_at",
        ]

        for record in response.data["results"]:

            for field in required_fields:

                self.assertIn(
                    field,
                    record,
                )

    # =====================================================
    # TEST 14 — Newest first
    # =====================================================

    def test_logs_are_ordered_newest_first(self):

        response = self.call_list()

        timestamps = [
            record["created_at"]
            for record in response.data["results"]
        ]

        self.assertEqual(
            timestamps,
            sorted(
                timestamps,
                reverse=True,
            ),
        )

    # =====================================================
    # TEST 15 — Model immutability
    # =====================================================

    def test_model_update_is_blocked(self):

        log = AuditLog.objects.get(
            id=self.log1.id
        )

        original = log.description

        log.description = "UNAUTHORIZED UPDATE"

        with self.assertRaises(ValueError):
            log.save()

        log.refresh_from_db()

        self.assertEqual(
            log.description,
            original,
        )

    # =====================================================
    # TEST 16 — Model deletion is blocked
    # =====================================================

    def test_model_delete_is_blocked(self):

        log = AuditLog.objects.get(
            id=self.log1.id
        )

        with self.assertRaises(ValueError):
            log.delete()

        self.assertTrue(
            AuditLog.objects.filter(
                id=self.log1.id
            ).exists()
        )

    # =====================================================
    # TEST 17 — API is read-only
    # =====================================================

    def test_api_is_read_only(self):

        view = AuditLogViewSet

        self.assertFalse(
            hasattr(view, "create")
        )

        self.assertFalse(
            hasattr(view, "update")
        )

        self.assertFalse(
            hasattr(view, "partial_update")
        )

        self.assertFalse(
            hasattr(view, "destroy")
        )