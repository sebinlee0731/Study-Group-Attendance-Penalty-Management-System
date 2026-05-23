from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import StudyMember, StudySchedule


class IsStudyLeader(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        schedule_id = request.data.get('schedule')

        if not schedule_id:
            return False

        schedule = StudySchedule.objects.filter(id=schedule_id).first()

        if not schedule:
            return False

        return StudyMember.objects.filter(
            study=schedule.study,
            user=request.user,
            role='leader'
        ).exists()