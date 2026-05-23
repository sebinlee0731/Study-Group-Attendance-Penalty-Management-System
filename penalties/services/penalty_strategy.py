class PenaltyStrategy:
    def calculate(self, rule):
        raise NotImplementedError


class PresentPenaltyStrategy(PenaltyStrategy):
    def calculate(self, rule):
        return 0, '출석'


class LatePenaltyStrategy(PenaltyStrategy):
    def calculate(self, rule):
        return rule.late_amount, '지각'


class AbsentPenaltyStrategy(PenaltyStrategy):
    def calculate(self, rule):
        return rule.absent_amount, '결석'


def get_penalty_strategy(status):
    if status == 'present':
        return PresentPenaltyStrategy()

    if status == 'late':
        return LatePenaltyStrategy()

    if status == 'absent':
        return AbsentPenaltyStrategy()

    return PresentPenaltyStrategy()