from .models import AuditLog


def create_audit_log(
    actor,
    action,
    target_table,
    target_id,
    description=None,
    old_value=None,
    new_value=None,
    reason=None
):
    AuditLog.objects.create(
        actor=actor,
        action=action,
        target_table=target_table,
        target_id=target_id,
        description=description,
        old_value=old_value,
        new_value=new_value,
        reason=reason
    )