from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from studies.models import Study, StudyMember, StudySchedule
from attendances.models import Attendance
from penalties.models import PenaltyRule, PenaltySettlement
from penalties.services.settlement_service import StandardSettlementService


class AttendancePenaltyTest(TestCase):

    def setUp(self):
        self.leader = User.objects.create_user(
            username='leader',
            password='1234'
        )

        self.member = User.objects.create_user(
            username='member',
            password='1234'
        )

        self.study = Study.objects.create(
            title='테스트 스터디',
            leader=self.leader
        )

        StudyMember.objects.create(
            study=self.study,
            user=self.leader,
            role='leader'
        )

        StudyMember.objects.create(
            study=self.study,
            user=self.member,
            role='member'
        )

        self.schedule = StudySchedule.objects.create(
            study=self.study,
            title='1회차',
            session_number=1,
            scheduled_at=timezone.now(),
            created_by=self.leader
        )

        self.rule = PenaltyRule.objects.create(
            study=self.study,
            late_amount=1000,
            absent_amount=3000,
            late_threshold_seconds=600,
            applied_from=timezone.now(),
            created_by=self.leader
        )

    def test_001_late_penalty_calculation(self):
        attendance = Attendance.objects.create(
            schedule=self.schedule,
            user=self.member,
            status='late',
            recorded_by=self.leader
        )

        settlement = StandardSettlementService().process(attendance)

        self.assertEqual(settlement.amount, 1000)
        self.assertEqual(settlement.reason, '지각')

    def test_002_absent_penalty_calculation(self):
        attendance = Attendance.objects.create(
            schedule=self.schedule,
            user=self.member,
            status='absent',
            recorded_by=self.leader
        )

        settlement = StandardSettlementService().process(attendance)

        self.assertEqual(settlement.amount, 3000)
        self.assertEqual(settlement.reason, '결석')

    def test_003_present_penalty_is_zero(self):
        attendance = Attendance.objects.create(
            schedule=self.schedule,
            user=self.member,
            status='present',
            recorded_by=self.leader
        )

        settlement = StandardSettlementService().process(attendance)

        self.assertEqual(settlement.amount, 0)
        self.assertEqual(settlement.reason, '출석')

    def test_004_duplicate_attendance_not_allowed(self):
        Attendance.objects.create(
            schedule=self.schedule,
            user=self.member,
            status='late',
            recorded_by=self.leader
        )

        with self.assertRaises(Exception):
            Attendance.objects.create(
                schedule=self.schedule,
                user=self.member,
                status='absent',
                recorded_by=self.leader
            )

    def test_005_penalty_settlement_created(self):
        attendance = Attendance.objects.create(
            schedule=self.schedule,
            user=self.member,
            status='late',
            recorded_by=self.leader
        )

        StandardSettlementService().process(attendance)

        exists = PenaltySettlement.objects.filter(
            attendance=attendance
        ).exists()

        self.assertTrue(exists)