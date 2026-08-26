from apps.audit_trail.models import AuditLog


def create_audit_log(
    *,
    user=None,
    action,
    module,
    object_type=None,
    object_id=None,
    description="",
    old_values=None,
    new_values=None,
    ip_address=None,
    user_agent=None,
    request_id=None,
):
    """
    Create an immutable IAPS audit log entry.
    """

    return AuditLog.objects.create(
        user=user,
        action=action,
        module=module,
        object_type=object_type,
        object_id=str(object_id) if object_id is not None else None,
        description=description,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent,
        request_id=request_id,
    )