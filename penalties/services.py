from penalties.services.settlement_service import StandardSettlementService


def create_penalty(attendance):
    service = StandardSettlementService()
    return service.process(attendance)