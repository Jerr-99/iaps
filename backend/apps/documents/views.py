from rest_framework import permissions, viewsets

from apps.documents.models import Document
from apps.documents.serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for audit documents.

    Provides:
        GET     /api/documents/
        POST    /api/documents/
        GET     /api/documents/{id}/
        PUT     /api/documents/{id}/
        PATCH   /api/documents/{id}/
        DELETE  /api/documents/{id}/
    """

    queryset = Document.objects.select_related(
        "engagement",
        "uploaded_by",
    ).all()

    serializer_class = DocumentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        """
        Automatically assign the authenticated user as uploader
        and create an immutable audit-trail entry.
        """

        document = serializer.save(
            uploaded_by=self.request.user,
        )

        from apps.audit_trail.services import create_audit_log

        create_audit_log(
            user=self.request.user,
            action="upload",
            module="documents",
            object_type="Document",
            object_id=str(document.id),
            description=(
                f"Document uploaded: "
                f"{document.name}."
            ),
            old_values={},
            new_values={
                "name": document.name,
                "document_type": document.document_type,
                "original_filename": document.original_filename,
                "file_size": document.file_size,
                "mime_type": document.mime_type,
                "processing_status": document.processing_status,
                "engagement_id": str(document.engagement_id),
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
        Update a document and create an immutable audit-trail entry
        containing the previous and new values.
        """

        document = self.get_object()

        # Capture values BEFORE the update.
        old_values = {
            "name": document.name,
            "description": document.description,
            "document_type": document.document_type,
            "processing_status": document.processing_status,
            "engagement_id": str(document.engagement_id),
        }

        # Perform the actual update.
        document = serializer.save()

        # Capture values AFTER the update.
        new_values = {
            "name": document.name,
            "description": document.description,
            "document_type": document.document_type,
            "processing_status": document.processing_status,
            "engagement_id": str(document.engagement_id),
        }

        from apps.audit_trail.services import create_audit_log

        create_audit_log(
            user=self.request.user,
            action="update",
            module="documents",
            object_type="Document",
            object_id=str(document.id),
            description=(
                f"Document updated: "
                f"{document.name}."
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
        Delete a document and create an immutable audit-trail entry
        containing the document values before deletion.
        """

        # Capture document values BEFORE deletion.
        old_values = {
            "name": instance.name,
            "description": instance.description,
            "document_type": instance.document_type,
            "original_filename": instance.original_filename,
            "file_size": instance.file_size,
            "mime_type": instance.mime_type,
            "processing_status": instance.processing_status,
            "engagement_id": str(instance.engagement_id),
            "uploaded_by": (
                instance.uploaded_by.username
                if instance.uploaded_by
                else None
            ),
        }

        document_id = str(instance.id)
        document_name = instance.name

        from apps.audit_trail.services import create_audit_log

        # Create the audit log BEFORE deleting the document.
        create_audit_log(
            user=self.request.user,
            action="delete",
            module="documents",
            object_type="Document",
            object_id=document_id,
            description=(
                f"Document deleted: "
                f"{document_name}."
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

        # Delete the actual document.
        instance.delete()