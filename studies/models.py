from django.db import models
from django.contrib.auth.models import User


class Study(models.Model):
    title = models.CharField(max_length=100)
    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='led_studies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class StudyMember(models.Model):

    ROLE_CHOICES = [
        ('leader', '팀장'),
        ('member', '팀원'),
    ]

    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='member'
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)


class StudySchedule(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    session_number = models.IntegerField()
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.title