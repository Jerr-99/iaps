"""Views for Financial app"""
from rest_framework import viewsets
from .models import FinancialData
from .serializers import FinancialDataSerializer
class FinancialDataViewSet(viewsets.ModelViewSet):
    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer
