"""Admin for Engagements app"""
from django.contrib import admin
from .models import Engagement
@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    list_display = ('id',)
