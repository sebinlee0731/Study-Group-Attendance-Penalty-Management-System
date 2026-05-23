from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from audits.services import create_audit_log
from studies.models import StudyMember

from .models import Objection
from .serializers import ObjectionSerializer
from .services.objection_state import get_objection_state


class ObjectionCreateView(generics.CreateAPIView):
    serializer_class = ObjectionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyObjectionListView(generics.ListAPIView):
    serializer_class = ObjectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Objection.objects.filter(user=self.request.user)


class ObjectionProcessView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, objection_id):
        objection = Objection.objects.get(id=objection_id)

        study = objection.settlement.attendance.schedule.study

        is_leader = StudyMember.objects.filter(
            study=study,
            user=request.user,
            role='leader'
        ).exists()

        if not is_leader:
            raise PermissionDenied('팀장만 이의 신청을 처리할 수 있습니다.')

        new_status = request.data.get('status')

        try:
            state = get_objection_state(objection.status)
            objection = state.process(objection, new_status)
        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=400)

        objection.reviewed_by = request.user
        objection.reviewed_at = timezone.now()
        objection.processed_at = timezone.now()
        objection.review_note = request.data.get('review_note', '')
        objection.save()

        create_audit_log(
            actor=request.user,
            action='UPDATE',
            target_table='objections',
            target_id=objection.id,
            description=f'이의 신청 {new_status} 처리',
            new_value={
                'status': objection.status,
                'review_note': objection.review_note
            },
            reason='이의 신청 검토'
        )

        return Response({
            "message": "이의 신청이 처리되었습니다.",
            "objection_id": objection.id,
            "status": objection.status,
            "reviewed_by": objection.reviewed_by.id if objection.reviewed_by else None,
            "reviewed_at": objection.reviewed_at,
            "review_note": objection.review_note,
            "processed_at": objection.processed_at
        })