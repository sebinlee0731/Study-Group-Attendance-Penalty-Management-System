# 스터디 그룹 출결 및 벌금 관리 시스템

스터디 그룹의 출결 관리와 벌금 정산을 자동화하기 위한 Django 기반 백엔드 시스템입니다.  
기존 카카오톡 투표 및 수동 엑셀 방식의 문제점을 개선하기 위해 출결 기록, 벌금 자동 계산, 납부 관리, 이의 신청, 감사 로그 기능을 통합 구현하였습니다.  

또한 유지보수성과 확장성을 높이기 위해 Factory, Facade, State, Signal 패턴 등 다양한 디자인 패턴을 적용하였습니다.

---

# 프로젝트 개요

기존 스터디 운영 방식에서는 출결 기록 누락, 벌금 계산 오류, 정산 내역 불투명성 등의 문제가 발생하였습니다.  
본 프로젝트는 이러한 문제를 해결하기 위해 출결 상태 기반 벌금 자동 정산 시스템을 구현하였으며, Django REST Framework 기반 API 서버 구조를 적용하였습니다.

특히 벌금 자동 생성 과정에서는 Factory Pattern을 적용하여 새로운 벌금 정책(지각, 결석, 조기 퇴장 등)이 추가되더라도 기존 코드를 수정하지 않고 확장할 수 있도록 설계하였습니다.

---

# Tech Stack

| Category | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Database | SQLite |
| Authentication | JWT |
| Architecture | Layered Architecture |
| Design Pattern | Factory, Facade, State, Signal |
| ORM | Django ORM |

---

# 주요 기능

## 출결 관리
- 스터디 일정 등록
- 팀원 출결 상태 입력
- 출결 수정 기능
- 출결 이력 조회

## 벌금 자동 정산
- 출결 상태 기반 자동 계산
- 지각 / 결석 벌금 규칙 관리
- 벌금 납부 여부 관리
- 누적 벌금 조회

## 이의 신청 시스템
- 벌금 및 출결 이의 신청
- 팀장 승인 / 거부 처리
- 상태 기반 처리(State Pattern)

## 감사 로그(Audit Log)
- 수정 내역 자동 저장
- 변경 전/후 데이터 기록
- 변경 사용자 및 시각 저장

---

# 디자인 패턴 적용

## 1. Factory Pattern

벌금 자동 생성 기능에서 Factory Pattern을 적용하여 벌금 생성 책임을 분리하였습니다.  
출결 상태(지각, 결석 등)에 따라 서로 다른 벌금 객체를 생성할 수 있도록 설계하였으며, 새로운 벌금 유형 추가 시 기존 코드 수정 없이 확장이 가능합니다.

### 핵심 코드

```python
from penalties.services.settlement_service import StandardSettlementService

def create_penalty(attendance):
    service = StandardSettlementService()
    return service.process(attendance)
