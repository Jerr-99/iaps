"""
User models for IAPS
Intelligent Audit Planning and Risk Assessment System
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class User(AbstractUser):
    """
    Custom IAPS user model.

    Extends Django's AbstractUser with:
    - IAPS RBAC roles
    - Email authentication/contact information
    - Department and job title
    - Two-factor authentication status
    - Audit-related user information
    - Additional timestamps
    """

    # =========================================================================
    # ROLE CONFIGURATION
    # =========================================================================

    ROLE_ADMIN = 'admin'
    ROLE_SUPERVISOR = 'supervisor'
    ROLE_AUDITOR = 'auditor'
    ROLE_FINANCE_MANAGER = 'finance_manager'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_SUPERVISOR, 'Audit Supervisor'),
        (ROLE_AUDITOR, 'Auditor'),
        (ROLE_FINANCE_MANAGER, 'Finance Manager'),
    )

    # =========================================================================
    # BASIC USER INFORMATION
    # =========================================================================

    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text='User email address.'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_AUDITOR,
        db_index=True,
        help_text='IAPS role assigned to the user.'
    )

    # =========================================================================
    # ACCOUNT STATUS
    # =========================================================================

    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user account is active.'
    )

    two_fa_enabled = models.BooleanField(
        default=False,
        help_text='Whether two-factor authentication is enabled.'
    )

    # =========================================================================
    # PROFESSIONAL INFORMATION
    # =========================================================================

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Department or organizational unit.'
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='User phone number.'
    )

    job_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='User job title.'
    )

    # =========================================================================
    # TIMESTAMPS
    # =========================================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    last_login_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Most recent successful login timestamp.'
    )

    # =========================================================================
    # META
    # =========================================================================

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

        indexes = [
            models.Index(
                fields=['email'],
                name='users_email_idx'
            ),

            models.Index(
                fields=['role'],
                name='users_role_idx'
            ),

            models.Index(
                fields=['department'],
                name='users_department_idx'
            ),

            models.Index(
                fields=['is_active'],
                name='users_active_idx'
            ),
        ]

    # =========================================================================
    # STRING REPRESENTATION
    # =========================================================================

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # =========================================================================
    # ROLE PROPERTIES
    # =========================================================================

    @property
    def is_admin(self):
        """
        Return True if the user is an administrator.
        """
        return self.role == self.ROLE_ADMIN

    @property
    def is_supervisor(self):
        """
        Return True if the user is an audit supervisor.
        """
        return self.role == self.ROLE_SUPERVISOR

    @property
    def is_auditor(self):
        """
        Return True if the user is an auditor.
        """
        return self.role == self.ROLE_AUDITOR

    @property
    def is_finance_manager(self):
        """
        Return True if the user is a finance manager.
        """
        return self.role == self.ROLE_FINANCE_MANAGER

    # =========================================================================
    # ROLE HELPER METHODS
    # =========================================================================

    def has_role(self, role):
        """
        Check whether the user has a specific IAPS role.

        Example:
            user.has_role('auditor')
        """
        return self.role == role

    def can_manage_users(self):
        """
        Determine whether the user can manage other users.
        """
        return self.role == self.ROLE_ADMIN

    def can_manage_engagements(self):
        """
        Determine whether the user can manage audit engagements.
        """
        return self.role in [
            self.ROLE_ADMIN,
            self.ROLE_SUPERVISOR,
        ]

    def can_manage_financial_data(self):
        """
        Determine whether the user can manage financial information.
        """
        return self.role in [
            self.ROLE_ADMIN,
            self.ROLE_SUPERVISOR,
            self.ROLE_FINANCE_MANAGER,
        ]

    def can_perform_audits(self):
        """
        Determine whether the user can perform audit activities.
        """
        return self.role in [
            self.ROLE_ADMIN,
            self.ROLE_SUPERVISOR,
            self.ROLE_AUDITOR,
        ]

    def can_manage_risk(self):
        """
        Determine whether the user can manage risk assessments.
        """
        return self.role in [
            self.ROLE_ADMIN,
            self.ROLE_SUPERVISOR,
            self.ROLE_AUDITOR,
        ]

    # =========================================================================
    # PROFILE
    # =========================================================================

    @property
    def full_name(self):
        """
        Return the user's full name.
        """
        return self.get_full_name().strip() or self.username


class UserProfile(models.Model):
    """
    Extended profile information for an IAPS user.

    This model stores information that does not belong directly
    on the authentication user model.
    """

    # =========================================================================
    # USER RELATIONSHIP
    # =========================================================================

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # =========================================================================
    # KEYCLOAK INTEGRATION
    # =========================================================================

    keycloak_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text='Keycloak user UUID.'
    )

    keycloak_username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Username stored in Keycloak.'
    )

    # =========================================================================
    # PROFILE INFORMATION
    # =========================================================================

    bio = models.TextField(
        blank=True,
        null=True
    )

    avatar_url = models.URLField(
        blank=True,
        null=True
    )

    preferred_language = models.CharField(
        max_length=10,
        default='en'
    )

    # =========================================================================
    # USER SETTINGS
    # =========================================================================

    email_notifications = models.BooleanField(
        default=True
    )

    dashboard_theme = models.CharField(
        max_length=20,

        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
        ],

        default='light'
    )

    # =========================================================================
    # TIMESTAMPS
    # =========================================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================================
    # META
    # =========================================================================

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    # =========================================================================
    # STRING REPRESENTATION
    # =========================================================================

    def __str__(self):
        return f"Profile of {self.user.username}"


class UserPermission(models.Model):
    """
    Custom fine-grained permissions for IAPS users.

    These are separate from Django's built-in permissions and
    can be used for application-specific authorization.
    """

    # =========================================================================
    # USER RELATIONSHIP
    # =========================================================================

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='custom_permissions'
    )

    # =========================================================================
    # PERMISSION INFORMATION
    # =========================================================================

    permission_code = models.CharField(
        max_length=255,
        help_text=(
            'Application permission code, '
            'for example: financial.view_transaction'
        )
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_granted = models.BooleanField(
        default=True
    )

    # =========================================================================
    # TIMESTAMPS
    # =========================================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================================
    # META
    # =========================================================================

    class Meta:
        verbose_name = 'User Permission'
        verbose_name_plural = 'User Permissions'

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'permission_code'
                ],
                name='unique_user_permission'
            ),
        ]

        indexes = [
            models.Index(
                fields=['permission_code'],
                name='userperm_code_idx'
            ),

            models.Index(
                fields=['user', 'is_granted'],
                name='userperm_granted_idx'
            ),
        ]

    # =========================================================================
    # STRING REPRESENTATION
    # =========================================================================

    def __str__(self):
        status = 'Granted' if self.is_granted else 'Denied'

        return (
            f"{self.user.username} - "
            f"{self.permission_code} - "
            f"{status}"
        )

    # =========================================================================
    # PERMISSION HELPER
    # =========================================================================

    def is_allowed(self):
        """
        Return whether this permission is currently granted.
        """
        return self.is_granted