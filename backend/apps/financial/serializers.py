"""Serializers for Financial app"""
from rest_framework import serializers
from .models import FinancialData
class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = '__all__'
