from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.audit_trail.models import AuditLog
from apps.documents.models import Document
from apps.engagements.models import Engagement
from apps.users.models import User


class DocumentAPITestCase(APITestCase):
    """
    API tests for the IAPS Documents module.

    Documents currently requires authentication but does not have
    module-specific RBAC. These tests verify authentication,
    CRUD behavior, file metadata capture, and audit-trail creation.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="auditor",
            email="auditor@example.com",
            password="TestPassword123!",
            role="auditor",
        )

        self.other_user = User.objects.create_user(
            username="supervisor",
            email="supervisor@example.com",
            password="TestPassword123!",
            role="supervisor",
        )

        from datetime import date

        self.engagement = Engagement.objects.create(
            engagement_code="ENG-DOC-001",
            title="Document Test Engagement",
            description="Engagement for document API testing.",
            department="Finance",
            auditee="NCDC",
            audit_year=2026,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            status="planning",
            risk_level="moderate",
            lead_auditor=self.user,
            created_by=self.user,
        )

        self.document = Document.objects.create(
            engagement=self.engagement,
            uploaded_by=self.user,
            name="Existing Document",
            description="Existing test document.",
            document_type="invoice",
            file=SimpleUploadedFile(
                "existing.pdf",
                b"existing document content",
                content_type="application/pdf",
            ),
            original_filename="existing.pdf",
            file_size=24,
            mime_type="application/pdf",
        )

        self.url = "/api/documents/"

    def authenticate(self, user=None):
        self.client.force_authenticate(
            user=user or self.user
        )

    def test_unauthenticated_user_cannot_view_documents(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_view_documents(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_authenticated_user_can_view_document_detail(self):
        self.authenticate()

        response = self.client.get(
            f"{self.url}{self.document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.document.id,
        )

    def test_authenticated_user_can_create_document(self):
        self.authenticate()

        uploaded_file = SimpleUploadedFile(
            "invoice.pdf",
            b"invoice test content",
            content_type="application/pdf",
        )

        response = self.client.post(
            self.url,
            {
                "engagement": self.engagement.id,
                "name": "New Invoice",
                "description": "Test invoice upload.",
                "document_type": "invoice",
                "file": uploaded_file,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        document = Document.objects.get(
            id=response.data["id"]
        )

        self.assertEqual(
            document.uploaded_by,
            self.user,
        )

        self.assertEqual(
            document.original_filename,
            "invoice.pdf",
        )

        self.assertEqual(
            document.mime_type,
            "application/pdf",
        )

        self.assertEqual(
            document.file_size,
            len(b"invoice test content"),
        )

    def test_create_document_creates_upload_audit_log(self):
        self.authenticate()

        uploaded_file = SimpleUploadedFile(
            "receipt.pdf",
            b"receipt content",
            content_type="application/pdf",
        )

        response = self.client.post(
            self.url,
            {
                "engagement": self.engagement.id,
                "name": "Receipt",
                "document_type": "receipt",
                "file": uploaded_file,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.user,
                action="upload",
                module="documents",
                object_type="Document",
                object_id=str(response.data["id"]),
            ).exists()
        )

    def test_authenticated_user_can_update_document(self):
        self.authenticate()

        response = self.client.patch(
            f"{self.url}{self.document.id}/",
            {
                "name": "Updated Document",
                "description": "Updated description.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.name,
            "Updated Document",
        )

        self.assertEqual(
            self.document.description,
            "Updated description.",
        )

    def test_update_document_creates_audit_log(self):
        self.authenticate()

        response = self.client.patch(
            f"{self.url}{self.document.id}/",
            {
                "name": "Audit Updated Document",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.user,
                action="update",
                module="documents",
                object_type="Document",
                object_id=str(self.document.id),
            ).exists()
        )

    def test_authenticated_user_can_delete_document(self):
        self.authenticate()

        document_id = self.document.id

        response = self.client.delete(
            f"{self.url}{document_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Document.objects.filter(
                id=document_id
            ).exists()
        )

    def test_delete_document_creates_audit_log(self):
        self.authenticate()

        document_id = self.document.id

        response = self.client.delete(
            f"{self.url}{document_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertTrue(
            AuditLog.objects.filter(
                user=self.user,
                action="delete",
                module="documents",
                object_type="Document",
                object_id=str(document_id),
            ).exists()
        )

    def test_document_processing_fields_are_read_only(self):
        self.authenticate()

        response = self.client.patch(
            f"{self.url}{self.document.id}/",
            {
                "processing_status": "completed",
                "extracted_text": "Injected extracted text",
                "processing_error": "Injected error",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.document.refresh_from_db()

        self.assertEqual(
            self.document.processing_status,
            "pending",
        )

        self.assertIsNone(
            self.document.extracted_text,
        )

        self.assertIsNone(
            self.document.processing_error,
        )
