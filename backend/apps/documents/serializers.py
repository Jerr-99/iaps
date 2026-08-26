from rest_framework import serializers

from apps.documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for documents uploaded to an audit engagement.

    The authenticated user is automatically assigned as
    uploaded_by by DocumentViewSet.perform_create().
    """

    engagement_code = serializers.CharField(
        source="engagement.engagement_code",
        read_only=True,
    )

    uploaded_by_username = serializers.CharField(
        source="uploaded_by.username",
        read_only=True,
    )

    class Meta:
        model = Document

        fields = [
            "id",
            "engagement",
            "engagement_code",
            "uploaded_by",
            "uploaded_by_username",
            "name",
            "description",
            "document_type",
            "file",
            "original_filename",
            "file_size",
            "mime_type",
            "processing_status",
            "extracted_text",
            "processing_error",
            "uploaded_at",
            "processed_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_by",
            "uploaded_by_username",
            "uploaded_at",
            "updated_at",
            "processed_at",
            "engagement_code",
            "file_size",
            "mime_type",
            "processing_status",
            "extracted_text",
            "processing_error",
        ]

    def create(self, validated_data):
        """
        Automatically capture file metadata when a document is uploaded.
        """

        uploaded_file = validated_data.get("file")

        if uploaded_file:
            validated_data["original_filename"] = uploaded_file.name
            validated_data["file_size"] = uploaded_file.size
            validated_data["mime_type"] = getattr(
                uploaded_file,
                "content_type",
                None,
            )

        return super().create(validated_data)