from penalties.models import PenaltyRule, PenaltySettlement
from .penalty_strategy import get_penalty_strategy


class BaseSettlementService:
    def process(self, attendance):
        self.validate(attendance)
        rule = self.get_rule(attendance)
        amount, reason = self.calculate(attendance, rule)
        return self.save(attendance, rule, amount, reason)

    def validate(self, attendance):
        if not attendance:
            raise ValueError('출결 데이터가 없습니다.')

    def get_rule(self, attendance):
        rule = PenaltyRule.objects.filter(
            study=attendance.schedule.study
        ).order_by('-applied_from').first()

        if not rule:
            raise ValueError('벌금 규칙이 없습니다.')

        return rule

    def calculate(self, attendance, rule):
        raise NotImplementedError

    def save(self, attendance, rule, amount, reason):
        settlement, created = PenaltySettlement.objects.get_or_create(
            attendance=attendance,
            defaults={
                'user': attendance.user,
                'rule': rule,
                'amount': amount,
                'reason': reason,
                'is_exempted': False
            }
        )

        if not created:
            settlement.user = attendance.user
            settlement.rule = rule
            settlement.amount = amount
            settlement.reason = reason
            settlement.save()

        return settlement


class StandardSettlementService(BaseSettlementService):
    def calculate(self, attendance, rule):
        strategy = get_penalty_strategy(attendance.status)
        return strategy.calculate(rule)