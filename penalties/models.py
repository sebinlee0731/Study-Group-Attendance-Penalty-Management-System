from django.db import models
from django.contrib.auth.models import User

from studies.models import Study
from attendances.models import Attendance


class PenaltyRule(models.Model):
    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE
    )

    late_amount = models.IntegerField(default=1000)

    absent_amount = models.IntegerField(default=3000)

    late_threshold_seconds = models.IntegerField(default=600)

    applied_from = models.DateTimeField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.study.title} 벌금 규칙'


class PenaltySettlement(models.Model):
    attendance = models.OneToOneField(
        Attendance,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rule = models.ForeignKey(
        PenaltyRule,
        on_delete=models.CASCADE
    )

    amount = models.IntegerField()

    is_exempted = models.BooleanField(default=False)

    exemption_reason = models.TextField(
        null=True,
        blank=True
    )

    reason = models.CharField(
        max_length=50,
        default='정산'
    )

    settled_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount}원'


class Payment(models.Model):
    STATUS_CHOICES = [
        ('unpaid', '미납'),
        ('paid', '납부 완료'),
        ('pending', '확인 대기'),
    ]

    settlement = models.OneToOneField(
        PenaltySettlement,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    paid_amount = models.IntegerField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='unpaid'
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    confirmed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_payments'
    )

    confirmed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.paid_amount}원 납부'