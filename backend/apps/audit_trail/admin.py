"""Admin for Audit Trail app"""
from django.contrib import admin
from .models import AuditLog
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id',)
