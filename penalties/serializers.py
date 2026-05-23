from rest_framework import serializers

from .models import (
    PenaltySettlement,
    Payment
)


class PenaltySettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PenaltySettlement
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = [
            'user',
            'status',
            'is_paid',
            'paid_at',
            'confirmed_by',
            'confirmed_at'
        ]