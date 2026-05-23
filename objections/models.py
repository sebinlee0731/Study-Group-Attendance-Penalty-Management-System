from django.db import models
from django.contrib.auth.models import User

from attendances.models import Attendance
from penalties.models import PenaltySettlement


class Objection(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기'),
        ('approved', '승인'),
        ('rejected', '거절'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    settlement = models.ForeignKey(
        PenaltySettlement,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_objections'
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    review_note = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user.username} - {self.status}'