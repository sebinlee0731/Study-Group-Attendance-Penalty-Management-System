from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'actor',
        'action',
        'target_table',
        'target_id',
        'created_at'
    )

    search_fields = (
        'target_table',
        'action',
        'description',
        'reason'
    )