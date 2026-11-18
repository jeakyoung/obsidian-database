---
title: Scheduler-Service 2차 리뷰 대응 중복id검증·트랜잭션경계 수정 11.17
date: 2026-11-17
type: 작업
project: SchedulerService
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# Scheduler-Service 2차 리뷰 대응 중복id검증·트랜잭션경계 수정 11.17

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 — reviewer 에이전트 2차 리뷰 결과 대응 |
| **요청일** | 2026-11-17 |
| **대상 시스템** | Scheduler-Service 백엔드 |
| **관련 화면·프로그램** | `ScheduleController`, `JdbcScheduleTargetDbConfigRepository`, `ScheduleExecutor` |

> 대상DB 다중선택 기능(T15~T21) 완료 시점에 reviewer가 발견한 Major 1건·Minor 2건을 수정. 1차 리뷰의 M1/M2는 재발하지 않았음을 재확인.

## 🔍 현상 및 원인

reviewer 2차 리뷰: (M4) `targetDbConfigIds` 배열에 중복 id가 섞이면 "존재 여부" 검증은 통과하지만 복합PK 위반 예외가 핸들러 없이 500으로 전파됨(React SPA 경로로는 도달 불가하지만 API 직접호출 경로에선 재현), (N4) 스케줄 생성/수정과 대상DB 연결 교체가 하나의 트랜잭션으로 안 묶여 있어 중간실패 시 "대상DB 0개" 불변조건이 일시적으로 깨질 수 있음, (N5) `executeForTargetDb`가 같은 대상DB를 두 번 조회.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| M4 | `validateTargetDbConfigIds` | `Set` 변환 후 크기 비교로 중복 발견 시 400 명시 거부 |
| N4 | `ScheduleController.create/update` | `@Transactional` 추가 — 스케줄 저장과 대상DB 연결 교체를 하나로 묶음 |
| N5 | `ScheduleExecutor.executeForTargetDb` | `findById` 1회만 호출해 결과 재사용 |

N4는 수정 전에 `@MockitoSpyBean`으로 `replaceForSchedule`이 실패하도록 스텁해 "재현 실패 확인 → 수정 → 통과" 순서를 지켰다.

## ✅ 검증 및 결과

- [x] 중복 id(`[5,5]`)로 생성/수정 시도 시 400(이전엔 500)
- [x] `replaceForSchedule` 실패 유도 시 스케줄 행도 커밋되지 않음(create)/원본값으로 롤백(update)
- [x] `mvn clean test` 120/120 그린

## 🔗 참고

- `.team/REVIEW.md` 2차 리뷰 (Scheduler-Service 레포)
- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] 스케줄당 대상DB 다중 선택과 부분실패 처리]]
