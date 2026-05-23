from django.db.models.signals import post_save
from django.dispatch import receiver

from attendances.models import Attendance
from penalties.models import PenaltySettlement
from .services import create_audit_log


@receiver(post_save, sender=Attendance)
def attendance_created_log(sender, instance, created, **kwargs):
    if created:
        create_audit_log(
            actor=instance.recorded_by,
            action='CREATE',
            target_table='attendances',
            target_id=instance.id,
            description=f'{instance.user.username} 출결 생성',
            new_value={
                'status': instance.status,
                'schedule_id': instance.schedule_id,
                'user_id': instance.user_id,
                'recorded_by_id': instance.recorded_by_id
            }
        )


@receiver(post_save, sender=PenaltySettlement)
def penalty_created_log(sender, instance, created, **kwargs):
    if created:
        create_audit_log(
            actor=instance.attendance.recorded_by,
            action='CREATE',
            target_table='penalty_settlements',
            target_id=instance.id,
            description=f'{instance.user.username} 벌금 생성',
            new_value={
                'attendance_id': instance.attendance_id,
                'user_id': instance.user_id,
                'rule_id': instance.rule_id,
                'amount': instance.amount,
                'reason': instance.reason,
                'is_exempted': instance.is_exempted
            }
        )