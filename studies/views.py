from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from objections.models import Objection
from penalties.models import PenaltySettlement
from audits.services import create_audit_log
from audits.models import AuditLog
from .models import Study, StudyMember, StudySchedule
from .serializers import (
    StudySerializer,
    StudyMemberSerializer,
    StudyScheduleSerializer
)

from attendances.models import Attendance
from penalties.models import PenaltySettlement
from penalties.services.settlement_service import StandardSettlementService


class StudyHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'studies/study_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        study = Study.objects.first()

        context['study'] = study
        context['schedules_count'] = StudySchedule.objects.filter(
            study=study
        ).count()

        context['attendances_count'] = Attendance.objects.filter(
            schedule__study=study
        ).count()

        context['total_penalty'] = sum(
            PenaltySettlement.objects.filter(
                attendance__schedule__study=study
            ).values_list('amount', flat=True)
        )

        return context


class AttendanceManagePageView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/attendance_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        study = Study.objects.first()
        schedule_id = self.request.GET.get('schedule_id')

        schedules = StudySchedule.objects.filter(study=study)
        selected_schedule = None
        members = []

        if schedule_id:
            selected_schedule = StudySchedule.objects.get(id=schedule_id)

            members = StudyMember.objects.filter(
                study=study,
                is_active=True
            )

        context['schedules'] = schedules
        context['selected_schedule'] = selected_schedule
        context['members'] = members

        return context

    def post(self, request, *args, **kwargs):
        schedule_id = request.POST.get('schedule_id')
        schedule = StudySchedule.objects.get(id=schedule_id)

        members = StudyMember.objects.filter(
            study=schedule.study,
            is_active=True
        )

        for member in members:
            status = request.POST.get(f'status_{member.user.id}')

            attendance, created = Attendance.objects.update_or_create(
                schedule=schedule,
                user=member.user,
                defaults={
                    'status': status,
                    'recorded_by': request.user
                }
            )

            if created:
                StandardSettlementService().process(attendance)

        messages.success(
            request,
            '출결이 저장되고 벌금이 자동 정산되었습니다.'
        )

        return redirect(f'/attendance/?schedule_id={schedule.id}')


class StudyListView(generics.ListAPIView):
    serializer_class = StudySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Study.objects.filter(
            studymember__user=self.request.user
        ).distinct()


class StudyDetailView(generics.RetrieveAPIView):
    serializer_class = StudySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Study.objects.filter(
            studymember__user=self.request.user
        ).distinct()


class StudyMemberListView(generics.ListAPIView):
    serializer_class = StudyMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        study_id = self.kwargs['study_id']

        return StudyMember.objects.filter(
            study_id=study_id
        )


class StudyScheduleListView(generics.ListAPIView):
    serializer_class = StudyScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        study_id = self.kwargs['study_id']

        return StudySchedule.objects.filter(
            study_id=study_id
        )
    
class FineDashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = 'fines/fine_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        settlements = PenaltySettlement.objects.select_related(
            'user',
            'attendance'
        ).all()

        total_amount = sum(
            settlement.amount for settlement in settlements
        )

        paid_amount = 0

        for settlement in settlements:
            payment = getattr(settlement, 'payment', None)

            if payment and payment.is_paid:
                paid_amount += settlement.amount

        unpaid_amount = total_amount - paid_amount

        context['settlements'] = settlements
        context['total_amount'] = total_amount
        context['paid_amount'] = paid_amount
        context['unpaid_amount'] = unpaid_amount

        return context
    
class AppealPageView(LoginRequiredMixin, TemplateView):
    template_name = 'appeals/appeal_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['settlements'] = PenaltySettlement.objects.select_related(
            'user',
            'attendance'
        ).all()

        context['objections'] = Objection.objects.select_related(
            'user',
            'settlement'
        ).all().order_by('-created_at')

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'create':
            settlement_id = request.POST.get('settlement_id')
            reason = request.POST.get('reason')

            settlement = PenaltySettlement.objects.get(id=settlement_id)

            Objection.objects.create(
                user=request.user,
                settlement=settlement,
                attendance=settlement.attendance,
                reason=reason,
                status='pending'
            )

            messages.success(request, '이의 신청이 접수되었습니다.')
            return redirect('/appeals/')

        if action == 'process':
            objection_id = request.POST.get('objection_id')
            new_status = request.POST.get('status')

            objection = Objection.objects.get(id=objection_id)

            objection.status = new_status
            objection.reviewed_by = request.user
            objection.reviewed_at = timezone.now()
            objection.processed_at = timezone.now()
            objection.review_note = '웹 화면에서 처리됨'
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
                reason='웹 화면 이의 신청 처리'
            )

            messages.success(request, '이의 신청이 처리되었습니다.')
            return redirect('/appeals/')

        return redirect('/appeals/')
    
class AuditLogPageView(LoginRequiredMixin, TemplateView):
    template_name = 'logs/audit_log.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logs = AuditLog.objects.select_related(
            'actor'
        ).all().order_by('-created_at')

        context['logs'] = logs

        return context