---
title: Scheduler-Service 반복주기UI·대상DB다중선택·업체별모아보기 구현 11.16-17
date: 2026-11-17
type: 작업
project: SchedulerService
status: 완료
priority: 매우높음
assignee:
  - 안재경
tags: []
---

# Scheduler-Service 반복주기UI·대상DB다중선택·업체별모아보기 구현 11.16-17

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 — 사용성·범용성 확장 요청 |
| **요청일** | 2026-11-16 ~ 11-17 |
| **대상 시스템** | Scheduler-Service 백엔드/프론트엔드 |
| **관련 화면·프로그램** | TASKS.md T15~T21 전체 |

> 신규 기능 3가지(구조화 cron 입력, 스케줄당 대상DB 다중선택, 업체별 모아보기)를 추가한 가장 큰 규모의 작업.

## 🔍 현상 및 원인

기존 cron 텍스트 입력은 관리자가 Quartz 문법을 알아야 해서 직관적이지 않았고, 스케줄은 대상DB 1개에 고정돼 있어서 같은 업체의 여러 지점 DB에 같은 SP를 돌리려면 스케줄을 여러 개 만들어야 했다. [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.17 대상DB 다중선택 기능요청]]에서 3가지 요청을 확정했다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 스키마(T15) | `V3__schedule_target_db_multi.sql` | `schedule_target_db_config` N:M 조인테이블 신설, 기존 1:1 FK 제거 |
| 도메인(T16) | `ScheduleTargetDbConfigRepository` | `findByScheduleId`/`replaceForSchedule` |
| 엔진(T17) | `ScheduleExecutor` | 대상DB 순차순회+부분실패허용 재작성, `ExecutionStatus.PARTIAL_SUCCESS` 신설, `TargetDbExecutionResult` 추가 |
| API(T18) | `ScheduleController` 등 | `targetDbConfigId`→`targetDbConfigIds` 배열 계약 전환 |
| 프론트(T19) | `CronBuilder.tsx`/`cronPatterns.ts` | 6가지 반복패턴 구조화입력+역변환+고급모드 폴백 |
| 프론트(T20) | `TargetDbConfigMultiSelect`, `RunResultModal` 등 | 대상DB 체크박스 다중선택, 결과화면 대상DB별 섹션 분리 |
| 테스트(T21) | 전체 | 레거시 3패턴 재검증 + 다중대상DB 신규 시나리오 2개 |

## ✅ 검증 및 결과

- [x] 대상DB 전부성공→SUCCESS, 일부성공→PARTIAL_SUCCESS, 전부실패→FAILURE
- [x] 한쪽 대상DB 실패가 다른 대상DB 순회를 막지 않음(mock 호출횟수 확인)
- [x] `DISPLAY_ONLY` 2개 대상DB 결과가 섞이지 않고 분리저장
- [x] 백엔드 `mvn test` 116/116, 프론트 `npm test` 25/25 그린

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] 스케줄당 대상DB 다중 선택과 부분실패 처리]]
- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] 반복주기 구조화 입력(CronBuilder)과 Quartz cron 변환]]
- `.team/TASKS.md` T15~T21 (Scheduler-Service 레포)
