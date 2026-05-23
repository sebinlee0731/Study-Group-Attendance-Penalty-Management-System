# 스터디 그룹 출결 및 벌금 관리 시스템

스터디 그룹의 출결 관리와 벌금 정산을 자동화하기 위한 Django 기반 백엔드 시스템입니다.
기존 카카오톡 투표 및 수동 엑셀 방식의 문제점을 개선하기 위해 출결 기록, 벌금 자동 계산, 납부 관리, 이의 신청, 감사 로그 기능을 통합 구현하였습니다.
또한 유지보수성과 확장성을 높이기 위해 Factory, Facade, State, Signal 패턴 등 다양한 디자인 패턴을 적용하였습니다.

---

## 📋 프로젝트 개요

기존 스터디 운영 방식에서는 출결 기록 누락, 벌금 계산 오류, 정산 내역 불투명성 등의 문제가 발생하였습니다.
본 프로젝트는 이러한 문제를 해결하기 위해 출결 상태 기반 벌금 자동 정산 시스템을 구현하였으며, Django REST Framework 기반 API 서버 구조를 적용하였습니다.

특히 벌금 자동 생성 과정에서는 **Factory Pattern**을 적용하여 새로운 벌금 정책(지각, 결석, 조기 퇴장 등)이 추가되더라도 기존 코드를 수정하지 않고 확장할 수 있도록 설계하였습니다.

---

## 🛠 Tech Stack

| Category | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Database | SQLite |
| Authentication | JWT |
| Architecture | Layered Architecture |
| Design Pattern | Factory, Facade, State, Signal |
| ORM | Django ORM |

---

## ✨ 주요 기능

### 출결 관리
- 스터디 일정 등록
- 팀원 출결 상태 입력
- 출결 수정 기능
- 출결 이력 조회

### 벌금 자동 정산
- 출결 상태 기반 자동 계산
- 지각 / 결석 벌금 규칙 관리
- 벌금 납부 여부 관리
- 누적 벌금 조회

### 이의 신청 시스템
- 벌금 및 출결 이의 신청
- 팀장 승인 / 거부 처리
- 상태 기반 처리 (State Pattern)

### 감사 로그 (Audit Log)
- 수정 내역 자동 저장
- 변경 전/후 데이터 기록
- 변경 사용자 및 시각 저장

---

## 🧩 디자인 패턴 적용

### 1. Factory Pattern

벌금 자동 생성 기능에서 Factory Pattern을 적용하여 벌금 생성 책임을 분리하였습니다.
출결 상태(지각, 결석 등)에 따라 서로 다른 벌금 객체를 생성할 수 있도록 설계하였으며, 새로운 벌금 유형 추가 시 기존 코드 수정 없이 확장이 가능합니다.

**핵심 코드**
```python
from penalties.services.settlement_service import StandardSettlementService

def create_penalty(attendance):
    service = StandardSettlementService()
    return service.process(attendance)
```

**처리 흐름**
```
Attendance 생성
    ↓
create_penalty()
    ↓
SettlementService.process()
    ↓
PenaltySettlement 생성
```

**적용 효과**
- 객체 생성 책임 분리
- 벌금 정책 확장 용이
- 유지보수성 향상
- 비즈니스 로직 캡슐화

---

### 2. Facade Pattern

출결 저장 → 벌금 자동 정산 → 로그 저장 흐름을 `AttendanceFacade`를 통해 단일 인터페이스로 처리하도록 구현하였습니다.

```python
facade = AttendanceFacade()

attendance = facade.record(
    validated_data=serializer.validated_data,
    request_user=request.user
)
```

**적용 효과**
- View 단순화
- 복잡한 처리 흐름 캡슐화
- 비즈니스 로직 분리

---

### 3. State Pattern

이의 신청 승인/거부 처리 시 현재 상태(`pending` / `approved` / `rejected`)에 따라 상태 객체를 생성하여 처리하도록 구현하였습니다.

```python
state = get_objection_state(objection.status)
objection = state.process(objection, new_status)
```

**적용 효과**
- 상태별 책임 분리
- 조건문 감소
- 상태 전환 로직 명확화

---

### 4. Signal Pattern

Django Signal(`post_save`)을 활용하여 출결 및 벌금 생성 시 감사 로그를 자동 저장하도록 구현하였습니다.

```python
@receiver(post_save, sender=Attendance)
def attendance_created_log(sender, instance, created, **kwargs):
    ...
```

**적용 효과**
- 이벤트 기반 처리
- Audit Logging 자동화
- 비즈니스 로직과 로그 저장 분리

---

## 🏗 시스템 아키텍처

```
Client
  ↓
URL Router
  ↓
Authentication / Permission Middleware
  ↓
Business Logic (views.py / services.py)
  ↓
Django ORM
  ↓
SQLite Database
```

**특징**
- 기능별 App 구조 분리
- REST API 기반 설계
- Layered Architecture 적용
- 서비스 계층 기반 구조 설계

---

## 📁 프로젝트 구조

```
accounts/
attendances/
audits/
objections/
penalties/
studies/

config/
manage.py
db.sqlite3
```

| App | Description |
|---|---|
| accounts | 사용자 인증 및 권한 |
| attendances | 출결 관리 |
| penalties | 벌금 계산 및 정산 |
| audits | 감사 로그 |
| objections | 이의 신청 처리 |
| studies | 스터디 및 멤버 관리 |

---

## 🗄 데이터베이스 구조

### 주요 테이블

| Table | Description |
|---|---|
| users | 사용자 및 권한 관리 |
| study_schedules | 스터디 일정 관리 |
| study_members | 스터디 멤버 관리 |
| attendances | 출결 상태 저장 |
| penalty_rules | 벌금 규칙 관리 |
| penalty_settlements | 벌금 자동 정산 결과 |
| payments | 벌금 납부 상태 |
| objections | 이의 신청 처리 |
| audit_logs | 감사 로그 저장 |

### 핵심 관계

```
Study
 └── StudyMember
      └── User

Attendance
 └── User
 └── Schedule

PenaltySettlement
 └── Attendance
 └── User
```

---

## 🔌 API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/studies/{id}/schedules/{id}/attendances` | 출결 입력 및 벌금 자동 정산 |
| GET | `/studies/{id}/fines` | 팀원별 벌금 조회 |
| PATCH | `/studies/{id}/attendances/{id}` | 출결 수정 및 재정산 |
| POST | `/studies/{id}/settlements/recalculate` | 벌금 재정산 |
| GET | `/studies/{id}/audit-logs` | 감사 로그 조회 |

---

## 🏆 핵심 성과

- 출결 기반 벌금 자동 정산 구현
- 디자인 패턴 기반 구조 설계
- 감사 로그 자동화 구현
- REST API 기반 서버 구축
- 유지보수 가능한 서비스 계층 구조 구현

---

## 🔭 향후 개선 사항

- PostgreSQL 기반 서버 배포
- Docker 컨테이너화
- 실시간 알림 기능 추가
- 출결 통계 대시보드 구현
- 대규모 트래픽 부하 테스트

---

## 👥 Team

- 강성현
- 김태연
- 심준용
- 이세빈
