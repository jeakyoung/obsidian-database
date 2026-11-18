---
title: Scheduler-Service 11.13 레거시 포팅 방향 교정
date: 2026-11-13
type: 회의록
project: SchedulerService
status: 완료
attendees:
  - 안재경
tags: []
---

# Scheduler-Service 11.13 레거시 포팅 방향 교정

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **일시** | 2026-11-13 |
| **장소** | (개인 작업, 세션) |
| **참석자** | 안재경 (+ Herdr sched-orchestrator/researcher) |
| **안건** | 리서치 방향이 레거시 포팅이 아니라 바닥부터 새 아키텍처 조사로 가고 있던 걸 교정 |

## 💬 논의 내용

researcher 에이전트가 레거시 코드를 깊이 들여다보지 않고 Quartz 등 범용 아키텍처 비교조사부터 진행하고 있는 걸 발견. 목표를 재확인: "바닥부터 새로 설계"가 아니라 레거시의 `SchedulerContextListener`(ScheduledExecutorService 기반 등록) + Task 패턴 + "SP 호출→결과가공→FCM 발송" 실행 흐름을 실제 코드 레벨에서 포팅/재사용하는 것.

## ✅ 결정 사항

| # | 결정 내용 | 근거 |
|:--|:--|:--|
| 1 | 바뀌는 건 딱 두 가지뿐 — (1) 하드코딩 Task 3개→DB 기반 동적 스케줄 정의, (2) `Config.java` 하드코딩→외부 설정 주입 | 나머지(SP호출/FCM payload 등)는 레거시 로직을 일반화해서 그대로 가져가야 범위가 과도하게 커지지 않음 |
| 2 | researcher를 중단시키고 레거시 소스를 실제로 읽은 뒤 재지시 | RESEARCH.md가 레거시 분석 없이 작성되고 있었음 |

## 🔜 후속 조치

| 조치 | 담당 | 기한 | 상태 |
|:--|:--|:--|:--|
| 레거시 소스(`SchedulerContextListener`/`DaySchedulerTask` 등) 읽고 RESEARCH.md 재작성 | sched-researcher | 즉시 | 완료 |

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/01_Tasks/Scheduler-Service 레거시 분석 및 범용 엔진 1차 구현 11.13]]
