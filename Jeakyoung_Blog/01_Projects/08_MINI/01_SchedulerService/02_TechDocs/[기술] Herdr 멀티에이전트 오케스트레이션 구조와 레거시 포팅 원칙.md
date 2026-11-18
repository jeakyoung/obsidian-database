---
title: Herdr 멀티에이전트 오케스트레이션 구조와 레거시 포팅 원칙
date: 2026-11-18
type: 기술문서
project: SchedulerService
status: 완료
category: 아키텍처
assignee:
  - 안재경
tags: []
---

# Herdr 멀티에이전트 오케스트레이션 구조와 레거시 포팅 원칙

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | Scheduler-Service (Herdr 세션) |
| **적용 범위** | 아키텍처 · 작업 프로세스 |
| **관련 모듈** | `.team/RESEARCH.md`/`PLAN.md`/`TASKS.md`/`LOG.md`/`REVIEW.md`, herdr CLI |

> 혼자서 researcher/planner/worker/reviewer 4개 역할의 sibling 에이전트를 herdr CLI로 직접 지시하며 설계→구현→리뷰를 반복한 구조. 이 프로젝트 전체가 이 구조로 진행됐다.

## 🎯 배경 및 요구사항

레거시 알림 스케줄러를 범용 엔진으로 포팅하는 작업을 혼자 끝까지 밀어붙이기 위해, 역할을 분리한 여러 AI 에이전트에게 작업을 위임하고 orchestrator로서 결과를 검증·교정하는 방식을 썼다. 각 에이전트는 herdr가 관리하는 별도 pane(터미널)에서 독립적인 Claude Code 세션으로 떠 있고, `herdr agent prompt <name> "<지시>" --wait`로 작업을 지시하고 `herdr agent read <name>`/`.team/LOG.md`로 결과를 확인한다.

## 🏗 설계 및 구현

### 구조

```
sched-orchestrator (나, w6:p2)
  ├─ sched-researcher (w6:p4)  — 조사만, 코드 작성 안 함
  ├─ sched-planner    (w6:p3)  — .team/PLAN.md·TASKS.md 설계만
  ├─ sched-worker      (w6:p5) — 실제 구현 + git commit(로컬만, push 금지)
  └─ sched-reviewer    (w6:p6) — 코드 리뷰 + .team/REVIEW.md 작성
```

- `.team/` 디렉터리가 공유 상태 저장소: `RESEARCH.md`(조사)→`PLAN.md`(설계, 근거 포함)→`TASKS.md`(작업분해+DoD)→`LOG.md`(worker가 매 작업 완료마다 append하는 타임스탬프 로그)→`REVIEW.md`(reviewer 결과).
- **레거시 포팅 원칙**: 레거시(`C:\Users\USER\Desktop\scheduler-test\scheduler-test`)는 절대 수정하지 않고 참고만 한다. "바뀌는 건 딱 두 가지뿐"(하드코딩 스케줄→DB 기반 동적 정의, `Config.java` 하드코딩→외부 설정 주입)이라는 원칙을 PLAN.md 맨 위에 못박아두고, 모든 설계 변경 시 이 원칙과의 관계를 명시하게 했다.
- **검증 가능성 원칙**: PLAN.md의 가정("A가 B에서도 동작할 것이다" 같은 문서상 주장)은 TASKS.md의 DoD에서 실측으로 검증하도록 강제했다. 예: "WAR 전환 후에도 `mvn spring-boot:run`이 되는지" 같은 것은 실제로 명령을 돌려서 확인하게 했다 — 문서 주장만으로 완료 처리하지 않음.

### 주요 로직 — 교정 루프

진행 중 사용자(나)가 방향을 여러 번 교정했는데, 매번 같은 패턴을 썼다:

1. 진행 중인 에이전트를 `herdr agent send-keys <name> esc`로 중단(작업 중이던 내용이 커밋/파일로 남기 전이면 손실 없음).
2. 교정된 지시를 다시 `herdr agent prompt`로 전달 — PLAN.md/TASKS.md부터 먼저 고치고 그 다음 worker에게 구현을 넘기는 순서를 지킴.
3. `.team/LOG.md`에 "무엇이 왜 바뀌었는지"를 orchestrator가 직접 기록.

```bash
herdr agent send-keys sched-researcher esc
herdr agent prompt sched-researcher "$(cat 교정지시.txt)" --wait --until working --until blocked --timeout 30000
```

> [!warning] bash 특수문자 이스케이프 문제
> `herdr agent prompt`에 긴 지시문을 직접 넘기다가 백틱(`` ` ``)이 bash 명령 치환으로 해석돼 지시문 일부가 깨진 적이 있었다. 이후로는 긴/특수문자 포함 지시문은 파일에 먼저 써두고 `$(cat file)`로 전달하는 방식으로 바꿨다.

## ✅ 검증

- [x] 레거시 코드를 실제로 참고했는지(수정 없이) — 전체 작업 기간 동안 레거시 디렉터리 변경 없음 확인
- [x] 다른 무관한 프로젝트 설정을 베끼지 않았는지 — ReeL-Trip의 Spring Boot 버전을 베낀 사례가 1건 발생했으나 사용자가 직접 발견해 Maven Central 메타데이터 직접조회로 재확정(→ [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.13 아키텍처 교정]])
- [x] 리뷰 루프가 실제로 결함을 잡는지 — 1차/2차 리뷰 모두 blocking은 없었지만 Major 1~2건씩 실제 결함 발견

## 🔗 참고

- `.team/RESEARCH.md`, `.team/PLAN.md`, `.team/TASKS.md`, `.team/LOG.md`, `.team/REVIEW.md` (Scheduler-Service 레포)
- [[01_Projects/08_MINI/01_SchedulerService/03_Meetings|회의록]] — 각 교정 세션 기록
