from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from audits.services import create_audit_log

from .models import (
    PenaltySettlement,
    Payment
)

from .serializers import (
    PenaltySettlementSerializer,
    PaymentSerializer
)


class PenaltyListView(generics.ListAPIView):
    serializer_class = PenaltySettlementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PenaltySettlement.objects.filter(
            attendance__user=self.request.user
        )


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        settlement = serializer.validated_data['settlement']

        serializer.save(
            user=settlement.user,
            status='unpaid',
            is_paid=False
        )

class PaymentCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)

        payment.is_paid = True
        payment.status = 'paid'
        payment.paid_at = timezone.now()
        payment.confirmed_by = request.user
        payment.confirmed_at = timezone.now()
        payment.save()

        create_audit_log(
            actor=request.user,
            action='UPDATE',
            target_table='payments',
            target_id=payment.id,
            description='벌금 납부 완료 처리',
            new_value={
                'status': payment.status,
                'is_paid': payment.is_paid,
                'paid_at': str(payment.paid_at)
            },
            reason='납부 확인'
        )

        return Response({
            "message": "납부 완료 처리되었습니다.",
            "payment_id": payment.id,
            "status": payment.status,
            "is_paid": payment.is_paid,
            "paid_at": payment.paid_at
        })