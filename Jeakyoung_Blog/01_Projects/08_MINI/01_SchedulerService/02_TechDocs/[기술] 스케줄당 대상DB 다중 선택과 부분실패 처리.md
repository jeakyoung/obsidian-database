---
title: 스케줄당 대상DB 다중 선택과 부분실패 처리
date: 2026-11-18
type: 기술문서
project: SchedulerService
status: 완료
category: 스케줄링엔진
assignee:
  - 안재경
tags: []
---

# 스케줄당 대상DB 다중 선택과 부분실패 처리

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | Scheduler-Service 백엔드 |
| **적용 범위** | 스케줄링 엔진 · 데이터 모델 |
| **관련 모듈** | `schedule_target_db_config`, `ScheduleExecutor`, `TargetDbExecutionResult`, `ExecutionStatus` |

> 스케줄 1개가 대상DB 1개에 고정되던 구조(1:1 FK)를, 등록된 대상DB 여러 개를 동시에 호출할 수 있는 N:M 구조로 바꿨다. 레거시엔 없던 완전히 신규 기능.

## 🎯 배경 및 요구사항

사용자 직접 요청: "지금 스케줄링처럼 전체 스케줄링 정보를 대상DB 1개에 고정하는 게 아니라, DB 정보를 여러 개 저장해두고 스케줄 생성 시 저장된 DB 커넥션을 여러 개 호출할 수도 있도록" — 한 업체 안에 지점별/사업부별로 여러 DB가 있고, 하나의 스케줄이 그 전부에 같은 SP를 돌려야 하는 경우를 지원해야 했다. 이어서 "업체(대상DB)별로 모아보기" 요구도 나와서, 실행결과를 대상DB 단위로 분리해서 보여줘야 했다.

## 🏗 설계 및 구현

### 구조

```sql
-- V3__schedule_target_db_multi.sql
CREATE TABLE schedule_target_db_config (
    schedule_id BIGINT NOT NULL,         -- FK, ON DELETE CASCADE
    target_db_config_id BIGINT NOT NULL, -- FK, ON DELETE 제한(참조중이면 삭제차단)
    PRIMARY KEY (schedule_id, target_db_config_id)
);
-- schedule_definition.target_db_config_id 컬럼/FK 제거 (아직 운영 전이라 데이터 백필 불필요)
```

```
ScheduleExecutor.doExecute(scheduleId)
  └─ ScheduleTargetDbConfigRepository로 대상DB id 목록 조회
       └─ for (각 대상DB) { 순차 순회, 병렬 아님 }
            try   { SP 호출 → ActionHandler.handle(...) → TargetDbExecutionResult(SUCCESS) }
            catch { TargetDbExecutionResult(FAILURE) — 다음 대상DB는 계속 진행 }
       └─ 집계: 전부 성공→SUCCESS, 전부 실패→FAILURE, 혼재→PARTIAL_SUCCESS(신규)
```

- **부분실패 허용(근거)**: 한 업체(대상DB)의 DB 장애·SP 오류가 다른 대상DB에 대한 실행까지 막으면 안 된다는 판단. 레거시도 애초에 "행 단위로 실패해도 나머지 행은 계속 FCM 발송"하는 정신이었다(한 HTTP 실패가 전체를 중단시키지 않음) — 같은 정신을 대상DB 단위로 확장했다.
- **순차 실행(병렬 아님)**: 레거시도 각 Task가 자신의 단일 DB를 순차 처리했고, 이 프로젝트 전제(단일 프로세스, 소수의 다운스트림 대상)에서는 병렬화 이득보다 스레드풀 관리/부분실패 순서보장의 단순성이 더 크다고 판단.
- **`ActionHandler`는 대상DB를 모른다**: "여러 대상DB를 안다"는 지식은 `ScheduleExecutor`에만 있고, `ApiCallActionHandler`/`DisplayOnlyActionHandler`는 여전히 "대상DB 1개분의 SP 결과를 처리한다"는 좁은 책임만 가진다 — 인터페이스 변경 없이 기능을 확장.
- **대상DB 데이터는 절대 섞지 않는다**: `groupingMode`(PER_ROW/GROUP_BY)도 대상DB 1개의 결과 안에서만 적용되고, `DisplayOutput`에 `targetDbConfigId`/`Name`을 태그해서 `DisplayOutputStore`의 키도 `(scheduleId, targetDbConfigId)` 복합키로 바꿨다 — 어느 업체 데이터인지 불분명해지는 걸 막기 위함.

### 주요 로직

```java
// ExecutionStatus 집계 규칙
SUCCESS         // 대상DB 전부 성공
PARTIAL_SUCCESS // 일부만 성공 (신규)
FAILURE         // 전부 실패, 또는 대상DB 순회를 시작도 못 한 경우
```

> [!warning] API 레벨 검증 공백 — 2차 리뷰에서 발견
> `targetDbConfigIds`에 같은 id가 중복으로 들어오면(예: `[5,5]`) 존재 여부 검증은 통과하지만 복합PK 위반 예외가 핸들러 없이 500으로 전파되던 결함(M4)이 있었다. `Set` 변환 후 크기 비교로 400을 명시적으로 던지도록 수정. React SPA(체크박스 다중선택)는 구조적으로 중복을 만들 수 없어 공식 경로로는 도달 불가했지만, API를 직접 호출하는 경로에선 재현됐다.

## ✅ 검증

- [x] 대상DB 전부 성공 → SUCCESS, 일부 성공 → PARTIAL_SUCCESS(실패한 것만 FAILURE 표시), 전부 실패 → FAILURE
- [x] 한 대상DB의 예외가 다른 대상DB 순회를 막지 않음(mock 호출횟수로 둘 다 실제 호출됐는지 확인)
- [x] `DISPLAY_ONLY` 스케줄이 대상DB 2개일 때 서로 다른 행 데이터가 섞이지 않고 분리저장됨(백엔드 통합테스트 + 프론트 RTL 테스트 양쪽)
- [x] 중복 대상DB id 입력 시 400(수정 전엔 500이었음 — 재현 후 수정 확인)
- [x] 스케줄 저장과 대상DB 연결 교체가 하나의 트랜잭션으로 묶여 원자적으로 롤백됨(의도적으로 실패를 유발해 재현 후 수정)

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Quartz 기반 동적 스케줄 등록·해제 구조]]
- [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.17 대상DB 다중선택 기능요청]]
- `.team/PLAN.md` §0/§3.1/§3.1b/§4.3b (Scheduler-Service 레포)
