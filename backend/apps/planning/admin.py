"""Admin for Planning app"""
from django.contrib import admin
from .models import AuditPlan
@admin.register(AuditPlan)
class AuditPlanAdmin(admin.ModelAdmin):
    list_display = ('id',)
