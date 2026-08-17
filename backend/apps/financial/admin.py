"""Admin for Financial app"""
from django.contrib import admin
from .models import FinancialData
@admin.register(FinancialData)
class FinancialDataAdmin(admin.ModelAdmin):
    list_display = ('id',)
