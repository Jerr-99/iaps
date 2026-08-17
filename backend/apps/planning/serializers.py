"""Serializers for Planning app"""
from rest_framework import serializers
from .models import AuditPlan
class AuditPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditPlan
        fields = '__all__'
