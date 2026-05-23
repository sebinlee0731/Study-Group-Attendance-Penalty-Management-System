from django.contrib import admin

from .models import (
    PenaltyRule,
    PenaltySettlement,
    Payment
)

admin.site.register(PenaltyRule)
admin.site.register(PenaltySettlement)
admin.site.register(Payment)