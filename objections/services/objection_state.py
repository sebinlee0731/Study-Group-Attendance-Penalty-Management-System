class ObjectionState:
    def process(self, objection, new_status):
        raise NotImplementedError


class PendingState(ObjectionState):
    def process(self, objection, new_status):
        if new_status not in ['approved', 'rejected']:
            raise ValueError('status는 approved 또는 rejected만 가능합니다.')

        objection.status = new_status
        return objection


class ApprovedState(ObjectionState):
    def process(self, objection, new_status):
        raise ValueError('이미 승인된 이의 신청은 다시 처리할 수 없습니다.')


class RejectedState(ObjectionState):
    def process(self, objection, new_status):
        raise ValueError('이미 거절된 이의 신청은 다시 처리할 수 없습니다.')


def get_objection_state(status):
    if status == 'pending':
        return PendingState()

    if status == 'approved':
        return ApprovedState()

    if status == 'rejected':
        return RejectedState()

    return PendingState()