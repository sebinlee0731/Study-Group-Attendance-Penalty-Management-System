from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    target_table = models.CharField(max_length=100)

    target_id = models.IntegerField()

    action = models.CharField(max_length=20)

    old_value = models.JSONField(
        null=True,
        blank=True
    )

    new_value = models.JSONField(
        null=True,
        blank=True
    )

    reason = models.TextField(
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.action} - {self.target_table}'