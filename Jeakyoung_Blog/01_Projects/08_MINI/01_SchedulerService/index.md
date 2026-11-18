---
date: 2026-11-18
title: Scheduler-Service
---

# Scheduler-Service

개인 미니 프로젝트. 회사의 레거시 알림 스케줄러(순수 서블릿+Tomcat, 자바 코드에 스케줄·비밀값이 하드코딩된 구조)를 참고해서, Herdr 기반 멀티에이전트(researcher/planner/worker/reviewer) 오케스트레이션으로 **범용 스케줄링 서비스**를 바닥부터 새로 설계·구현.

**프로젝트 목표**: "SP 호출 → 다운스트림 처리(API 호출 또는 웹 표시) → 결과 확인"이라는 레거시의 실행 흐름은 그대로 포팅하되, (1) 스케줄을 자바 코드가 아니라 DB에 저장해 런타임에 동적으로 추가/변경/삭제, (2) 비밀값을 소스에 하드코딩하지 않고 외부 설정으로 주입, 두 가지만 바꿔서 어떤 업체에 재배포해도 재컴파일 없이 쓸 수 있는 범용 엔진을 만드는 것.

**담당 범위**: 설계부터 구현·보안리뷰·배포 전환까지 전부 — orchestrator(나) 역할로 Herdr의 sibling 에이전트 4개(researcher/planner/worker/reviewer)에게 작업을 위임하고, 결과를 검증하고 사용자(나 자신)의 방향 교정을 받아 다음 단계로 넘기는 과정을 끝까지 수행.

## 기술 스택

| 항목 | 내용 |
|:--|:--|
| **담당 업무** | 범용 스케줄링 서비스 설계·구현·리뷰·배포전환 (1인 멀티에이전트 오케스트레이션) |
| **백엔드** | Java 17, Spring Boot 3.5.16, Quartz(JDBC JobStore), Spring JDBC, Spring Security(JWT) |
| **프론트엔드** | React (Vite + TypeScript) |
| **데이터베이스** | SQL Server(메타DB/대상DB), 로컬 개발은 H2 fallback |
| **배포** | 외부 Tomcat에 단일 WAR (백엔드+프론트 통합) |
| **참고 레거시** | 순수 서블릿(Tomcat) 기반 알림 스케줄러 — `ScheduledExecutorService` + 하드코딩 Task 3개 |

> [!note] 레거시는 읽기 전용 참고일 뿐, 이 저장소에 코드를 가져온 게 아니다
> 레거시 프로젝트는 끝까지 수정하지 않고 참고만 했다. "실행 흐름(SP 호출→다운스트림)"이라는 **패턴**만 포팅했고, 회사 전용 SP명/테이블명/비밀값은 전혀 가져오지 않았다(리뷰 단계에서 grep으로 0건 확인).

> [!note] Herdr 멀티에이전트 오케스트레이션으로 진행
> 혼자서 researcher/planner/worker/reviewer 4개 역할을 가진 sibling 에이전트를 직접 지시하며 진행했다. 중간에 방향을 여러 번 교정(바닥부터 새 설계가 아니라 레거시 포팅이 목표라는 점, 백엔드/프론트 분리, 대상DB 다중선택 등)했고, 리뷰어가 2라운드에 걸쳐 보안 결함(SQL 인젝션, 비밀값 마스킹 등)을 실제로 잡아냈다. 자세한 내용은 [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Herdr 멀티에이전트 오케스트레이션 구조와 레거시 포팅 원칙]] 참고.

## 문서 분류

- [[01_Projects/08_MINI/01_SchedulerService/01_Tasks|작업 목록]] - 레거시 분석·1차 구현, 보안리뷰 대응 2회, 대상DB 다중선택·반복주기UI 구현, 디자인 폴리싱, Tomcat WAR 배포 전환
- [[01_Projects/08_MINI/01_SchedulerService/05_Docs|프로젝트 문서]] - 프로젝트 개요, 개발 과정(git 로그 기반 타임라인)
- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs|기술 문서]] - 오케스트레이션 구조, Quartz 동적 스케줄링, 대상DB 다중선택·부분실패, 비밀값 2계층 설정, CronBuilder, JWT 인증·로컬개발 편의기능, Tomcat 단일 WAR 배포
- [[01_Projects/08_MINI/01_SchedulerService/03_Meetings|회의록]] - 방향 교정·기능범위 확정 세션 기록
- [[01_Projects/08_MINI/01_SchedulerService/04_References|참고 자료]] - 확인 필요·알아두면 좋은 점 체크리스트
