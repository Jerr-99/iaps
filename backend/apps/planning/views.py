"""Views for Planning app"""
from rest_framework import viewsets
from .models import AuditPlan
from .serializers import AuditPlanSerializer
class AuditPlanViewSet(viewsets.ModelViewSet):
    queryset = AuditPlan.objects.all()
    serializer_class = AuditPlanSerializer
