from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from attendances.models import Attendance
from penalties.services.settlement_service import StandardSettlementService
from studies.models import StudyMember


class AttendanceFacade:
    def __init__(self):
        self.settlement_service = StandardSettlementService()

    @transaction.atomic
    def record(self, validated_data, request_user):
        schedule = validated_data['schedule']

        is_leader = StudyMember.objects.filter(
            study=schedule.study,
            user=request_user,
            role='leader'
        ).exists()

        if not is_leader:
            raise PermissionDenied('팀장만 출결을 입력할 수 있습니다.')

        attendance = Attendance.objects.create(
            schedule=validated_data['schedule'],
            user=validated_data['user'],
            status=validated_data['status'],
            checked_in_at=validated_data.get('checked_in_at'),
            recorded_by=request_user
        )

        self.settlement_service.process(attendance)

        return attendance