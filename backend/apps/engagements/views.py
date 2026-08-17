"""Views for Engagements app"""
from rest_framework import viewsets
from .models import Engagement
from .serializers import EngagementSerializer
class EngagementViewSet(viewsets.ModelViewSet):
    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer
