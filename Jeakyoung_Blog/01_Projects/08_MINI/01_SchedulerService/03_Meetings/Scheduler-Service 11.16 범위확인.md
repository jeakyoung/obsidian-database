---
title: Scheduler-Service 11.16 범위확인
date: 2026-11-16
type: 회의록
project: SchedulerService
status: 완료
attendees:
  - 안재경
tags: []
---

# Scheduler-Service 11.16 범위확인

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **일시** | 2026-11-16 |
| **장소** | (개인 작업, 세션) |
| **참석자** | 안재경 |
| **안건** | Flyway 적용대상 오해 해소, 대상DB는 MSSQL 고정, SP 생성(DDL) 기능 범위제외 확정 |

## 💬 논의 내용

"Flyway를 왜 쓰는지, 신규 DB를 구축해서 마이그레이션할 일이 없지 않은지" 질문 → Flyway는 엔진 자신의 메타DB에만 적용되고 대상 업무 DB에는 전혀 적용되지 않는다는 기존 설계와 일치함을 확인(오해 해소). 이어서 "업체마다 다른 연결정보는 관리자 웹에서 입력받고, DB는 모든 솔루션이 MSSQL"이라는 확인이 나와 멀티-DBMS 지원(`db_type` 컬럼)을 제거하기로 했다. "SP를 생성하거나 호출하거나"의 '생성'이 신규 SP 생성(DDL) 기능까지 의미하는지 질문했고, 보류하기로 확정됐다.

## ✅ 결정 사항

| # | 결정 내용 | 근거 |
|:--|:--|:--|
| 1 | Flyway는 메타DB에만 적용, 대상 업무DB엔 적용 안 됨(기존 설계 그대로) | 오해였을 뿐, 설계 변경 없음 |
| 2 | `target_db_config.db_type` 컬럼 제거, MSSQL로 고정 | 대상 DB가 전부 MSSQL이라 멀티-DBMS 지원이 불필요한 범용성 |
| 3 | 대상 업무 DB에 대한 DDL/신규 SP 생성 기능은 범위 제외(이번뿐 아니라 앞으로도) | "의미 없을 것 같다"는 사용자 판단, 기존 SP 호출만 지원 |

## 🔜 후속 조치

| 조치 | 담당 | 기한 | 상태 |
|:--|:--|:--|:--|
| PLAN.md §1/§4.3/§9 수정, 마이그레이션에서 db_type 제거 | sched-planner → sched-worker | 즉시 | 완료 |

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/04_References/Scheduler-Service 확인 필요·알아두면 좋은 점 목록]]
