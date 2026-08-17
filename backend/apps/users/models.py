"""
User models for IAPS
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class User(AbstractUser):
    """
    Extended User model with RBAC roles
    """
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('supervisor', 'Audit Supervisor'),
        ('auditor', 'Auditor'),
        ('finance_manager', 'Finance Manager'),
    )
    
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='auditor')
    is_active = models.BooleanField(default=True)
    two_fa_enabled = models.BooleanField(default=False)
    
    # Profile information
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_supervisor(self):
        return self.role == 'supervisor'
    
    @property
    def is_auditor(self):
        return self.role == 'auditor'
    
    @property
    def is_finance_manager(self):
        return self.role == 'finance_manager'


class UserProfile(models.Model):
    """
    Extended user profile with Keycloak integration
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    keycloak_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    keycloak_username = models.CharField(max_length=255, blank=True, null=True)
    
    # Profile data
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default='en')
    
    # Settings
    email_notifications = models.BooleanField(default=True)
    dashboard_theme = models.CharField(
        max_length=20,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class UserPermission(models.Model):
    """
    Custom permissions for fine-grained access control
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_permissions')
    permission_code = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_granted = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'permission_code')
        verbose_name = 'User Permission'
        verbose_name_plural = 'User Permissions'
    
    def __str__(self):
        return f"{self.user.username} - {self.permission_code}"
