"""
API views for IAPS financial data.
"""

from rest_framework import permissions, viewsets

from apps.financial.models import FinancialData
from apps.financial.serializers import FinancialDataSerializer


class FinancialDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for financial transaction records.
    """

    queryset = FinancialData.objects.select_related(
        "engagement",
        "imported_by",
    ).all()

    serializer_class = FinancialDataSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        """
        Automatically assign the authenticated user as the importer.
        """

        serializer.save(
            imported_by=self.request.user,
        )