"""Admin for Risk app"""
from django.contrib import admin
from .models import Risk
@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('id',)
