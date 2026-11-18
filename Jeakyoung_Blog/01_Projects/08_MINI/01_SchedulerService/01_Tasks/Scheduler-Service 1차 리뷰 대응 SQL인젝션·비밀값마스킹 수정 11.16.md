---
title: Scheduler-Service 1차 리뷰 대응 SQL인젝션·비밀값마스킹 수정 11.16
date: 2026-11-16
type: 작업
project: SchedulerService
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# Scheduler-Service 1차 리뷰 대응 SQL인젝션·비밀값마스킹 수정 11.16

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 — reviewer 에이전트 1차 리뷰 결과 대응 |
| **요청일** | 2026-11-16 |
| **대상 시스템** | Scheduler-Service 백엔드 |
| **관련 화면·프로그램** | `StoredProcedureInvoker`, `Masking`, `BodyTemplateRenderer`, `ScheduleExecutionController` |

> T1~T14 완료 시점에 reviewer가 발견한 Major 2건·Minor 3건을 전부 수정.

## 🔍 현상 및 원인

reviewer가 `.team/REVIEW.md` 1차 리뷰에서: (M1) `StoredProcedureInvoker`가 SP명을 SQL 문자열에 그대로 이어붙여 SQL 인젝션 표면이 됨, (M2) `Masking.lastFour`가 4자 이하 비밀값을 마스킹 없이 그대로 노출, (N1) `BodyTemplateRenderer`가 JSON 이스케이프 없이 치환해 바디 깨짐/필드주입 가능, (N3) run-now/last-result가 실패한 실행에도 이전 성공결과를 그대로 반환, (N2) PLAN.md의 cron 문서가 Quartz 고유규칙을 언급 안 함 — 을 발견.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| M1 | `SqlIdentifierValidator`(신규) | SQL Server 식별자 화이트리스트 검증, 컨트롤러+Invoker 양쪽에 방어심층 적용 |
| M2 | `Masking.lastFour` | 4자 이하 값은 전체 마스킹하도록 분기 추가 |
| N1 | `BodyTemplateRenderer` | 바디 전용 `renderJson(...)` 신설(Jackson 이스케이프), 헤더용 `render()`는 무이스케이프 유지 |
| N3 | `ScheduleExecutionController` | `status != SUCCESS`면 `displayOutput`을 무조건 `null` 반환하도록 교체 |
| N2 | `.team/PLAN.md` | §4.1/§8에 Quartz cron day-of-month/day-of-week `?` 규칙 명시 |

각 수정마다 리뷰가 제시한 재현 페이로드(`"sp_test; DROP TABLE ...; --"`, `"4002"`, `EA_TITLE` 특수문자 등)로 먼저 재현을 확인한 뒤 수정했다.

## ✅ 검증 및 결과

- [x] 악의적 `spName`으로 스케줄 생성 시 400 거부
- [x] 4자리 비밀값이 전체 마스킹(`"****"`)됨
- [x] 특수문자 포함 컬럼값이 올바른 JSON으로 이스케이프됨(실제 HTTP 호출로 확인)
- [x] 실제로 SP를 DROP해 실행을 실패시킨 뒤 `displayOutput`이 `null`임을 확인
- [x] `mvn test` 97/97 그린

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/04_References/Scheduler-Service 확인 필요·알아두면 좋은 점 목록]]
- `.team/REVIEW.md` 1차 리뷰 (Scheduler-Service 레포)
