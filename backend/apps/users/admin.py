"""
Admin configuration for Users app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserPermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('IAPS Specific', {
            'fields': ('role', 'two_fa_enabled', 'department', 'phone_number', 'job_title')
        }),
    )
    list_display = ['username', 'email', 'role', 'is_active', 'two_fa_enabled', 'created_at']
    list_filter = ['role', 'is_active', 'two_fa_enabled', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model
    """
    list_display = ['user', 'keycloak_username', 'preferred_language', 'email_notifications']
    list_filter = ['preferred_language', 'email_notifications', 'dashboard_theme']
    search_fields = ['user__username', 'user__email', 'keycloak_username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """
    Admin interface for UserPermission model
    """
    list_display = ['user', 'permission_code', 'is_granted', 'created_at']
    list_filter = ['is_granted', 'created_at']
    search_fields = ['user__username', 'permission_code']
    readonly_fields = ['created_at', 'updated_at']
