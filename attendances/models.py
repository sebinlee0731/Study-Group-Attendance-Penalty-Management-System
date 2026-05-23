from django.db import models
from django.contrib.auth.models import User
from studies.models import StudySchedule


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', '출석'),
        ('late', '지각'),
        ('absent', '결석'),
    ]

    schedule = models.ForeignKey(
        StudySchedule,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    checked_in_at = models.DateTimeField(
        null=True,
        blank=True
    )

    recorded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recorded_attendances'
    )

    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('schedule', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.status}'