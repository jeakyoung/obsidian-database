---
title: Scheduler-Service 레거시 분석 및 범용 엔진 1차 구현 11.13
date: 2026-11-13
type: 작업
project: SchedulerService
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# Scheduler-Service 레거시 분석 및 범용 엔진 1차 구현 11.13

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인(개인 미니 프로젝트) |
| **요청일** | 2026-11-13 |
| **대상 시스템** | Scheduler-Service(신규), 레거시 알림 스케줄러(참고) |
| **관련 화면·프로그램** | TASKS.md T1~T14 전체 |

> 레거시의 "SP 호출→결과가공→FCM 발송" 실행 흐름을 분석해 Quartz+Spring Boot 기반 범용 엔진으로 포팅한 1차 구현 전체.

## 🔍 현상 및 원인

레거시(순수 서블릿+Tomcat)는 `SchedulerContextListener`가 `DaySchedulerTask`/`HourSchedulerTask`/`PurchaseReqSchedulerTask` 3개를 `ScheduledExecutorService`에 하드코딩 등록하고, `Config.java`에 DB·FCM 접속정보가 자바 상수로 박혀 있어서 환경을 바꾸려면 재컴파일이 필요했다. 리서치 에이전트가 처음엔 이 레거시를 깊이 안 보고 범용 아키텍처 비교조사부터 시작해서 방향을 교정해야 했다([[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.13 레거시 포팅 방향 교정]]).

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 리서치 | `.team/RESEARCH.md` | Quartz+JDBC JobStore, 2계층 비밀값 주입, Java17+Spring Boot3.x+Quartz+SQLServer 스택 추천 |
| 설계 | `.team/PLAN.md`/`TASKS.md` | §0 멀티테넌시 비채택, ExecutionResult/Sink 경계, DB스키마 5개 테이블, action_config JSON 2모양, T1~T14 작업분해 |
| 구현 | `backend/` | Maven 스캐폴딩(T1, 이후 backend/+thymeleaf제거로 재작업), Flyway 마이그레이션(T3), 도메인/Repository(T4), AES-256-GCM 암복호화(T5), 실행엔진 코어(T6), Quartz 동적등록(T7), 스케줄/대상DB/자격증명 CRUD API(T8~T10), JWT 인증(T11) |
| 구현 | `frontend/` | React SPA 8개 화면 스캐폴딩(T2) 및 실제 구현(T12) |
| 점검 | 전체 | 비밀값 최종점검(T13), 레거시 3패턴 회귀테스트(T14) |

중간에 백엔드/프론트 분리·React·JWT 결정(아키텍처 교정, [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.13 아키텍처 교정]])과 기능범위 6가지 확정([[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.13 기능범위 2차 교정]])이 끼어들어 재작업이 있었다.

## ✅ 검증 및 결과

- [x] `mvn test` 전체 그린(T14 시점 기준)
- [x] 레거시 3패턴(주1회그룹발송/평일30분개별발송/평일1일1회개별발송)을 신규 스케줄 정의로 재현하는 시나리오 테스트 3개 통과
- [x] 비밀값 리터럴 레포 전체 grep 0건

## 🔗 참고

- [[Scheduler-Service 프로젝트 개요]]
- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Quartz 기반 동적 스케줄 등록·해제 구조]]
- `.team/LOG.md`, `.team/TASKS.md` T1~T14 (Scheduler-Service 레포)
