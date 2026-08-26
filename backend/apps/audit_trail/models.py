from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """
    Immutable record of an important action performed in IAPS.

    The log identifies:
    - who performed the action
    - what action was performed
    - which application/module was affected
    - which object was affected
    - when the action occurred
    - relevant request/network information
    - optional before/after values
    """

    ACTION_CHOICES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("view", "View"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("upload", "Upload"),
        ("download", "Download"),
        ("approve", "Approve"),
        ("reject", "Reject"),
        ("process", "Process"),
        ("analyze", "Analyze"),
        ("export", "Export"),
        ("other", "Other"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audit_logs",
        blank=True,
        null=True,
    )

    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
    )

    module = models.CharField(
        max_length=100,
        help_text="IAPS module where the action occurred.",
    )

    object_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Type of object affected by the action.",
    )

    object_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Identifier of the affected object.",
    )

    description = models.TextField(
        help_text="Human-readable description of the action.",
    )

    old_values = models.JSONField(
        blank=True,
        null=True,
        help_text="Previous values before an update.",
    )

    new_values = models.JSONField(
        blank=True,
        null=True,
        help_text="New values after an update.",
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    user_agent = models.TextField(
        blank=True,
        null=True,
    )

    request_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Identifier used to correlate an action with a request.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["module"]),
            models.Index(fields=["object_type", "object_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        username = self.user.username if self.user else "System"
        return f"{username} - {self.action} - {self.module}"

    def save(self, *args, **kwargs):
        """
        Allow creation of audit logs but prevent modification
        of an existing audit log.
        """
        if self.pk:
            raise ValueError(
                "Audit logs are immutable and cannot be modified."
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Prevent deletion of audit logs.
        """
        raise ValueError(
            "Audit logs are immutable and cannot be deleted."
        )