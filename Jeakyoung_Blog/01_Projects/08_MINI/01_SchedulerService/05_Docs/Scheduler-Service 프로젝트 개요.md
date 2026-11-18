---
title: Scheduler-Service 프로젝트 개요
date: 2026-11-18
type: 프로젝트문서
project: SchedulerService
status: 진행중
tags: []
---

# Scheduler-Service 프로젝트 개요

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **프로젝트** | Scheduler-Service |
| **기간** | 2026-11 ~ 진행중 |
| **역할** | 설계·구현·리뷰·배포전환 전체 (Herdr 멀티에이전트 오케스트레이션) |
| **기술 스택** | Java 17, Spring Boot 3.5.16, Quartz, React, SQL Server/H2, Tomcat(WAR) |

> 회사의 레거시 알림 스케줄러를 참고해서, 자바 코드에 하드코딩됐던 스케줄·비밀값을 DB/외부설정으로 빼는 범용 스케줄링 엔진을 개인 미니 프로젝트로 처음부터 끝까지 만들었다.

## 🎯 목표 및 범위

레거시(`C:\Users\USER\Desktop\scheduler-test\scheduler-test`)는 Tomcat에 올라가는 순수 서블릿 애플리케이션으로, `SchedulerContextListener`가 `ScheduledExecutorService`에 `DaySchedulerTask`/`HourSchedulerTask`/`PurchaseReqSchedulerTask` 3개 클래스를 직접 등록하고, `Config.java`에 DB 접속정보·FCM API 키가 자바 상수로 하드코딩돼 있었다. 각 Task는 "SP 호출 → 결과 가공 → FCM 발송" 패턴이었다.

이 프로젝트의 목표는 그 **실행 흐름(패턴) 자체는 그대로 포팅**하면서 딱 두 가지만 바꾸는 것이었다:

1. 자바 코드에 하드코딩된 스케줄을 DB 기반 동적 스케줄 정의로 교체 — 관리자 웹에서 Create/Update/Delete, 재시작 없이 반영.
2. `Config.java`의 비밀값 하드코딩을 외부 설정 주입(부트스트랩은 환경변수, 운영값은 관리자 웹 CRUD)으로 교체.

나머지(SP 호출, 다운스트림 처리, 중복실행 방지 등)는 레거시 로직을 일반화해서 그대로 가져가는 것이 원칙이었다. 진행 중 사용자(나) 직접 지시로 범위가 몇 차례 확장됐다 — 백엔드/프론트 완전 분리(React SPA), JWT 인증, **스케줄당 대상DB 다중 선택**(한 스케줄이 여러 업체 DB에 동시에 SP를 호출), **알람식 반복주기 입력 UI**(cron 문법 대신 구조화 입력), 그리고 마지막엔 실제 배포 가능한 인프라가 **Tomcat뿐**이라는 제약에 따라 **단일 WAR 통합 배포**로 전환.

| 영역 | 범위 |
|:--|:--|
| **엔진 코어** | Quartz 동적 스케줄 등록/해제, SP 호출(파라미터 있음/없음), 다운스트림 2모드(API_CALL/DISPLAY_ONLY), 대상DB 다중선택+부분실패 허용 |
| **관리자 웹** | 스케줄 CRUD, 대상DB/자격증명 설정, 즉시실행, 로그인(JWT) |
| **범위 밖** | 실행이력 영속화(TBD, 미래 라운드), 복잡한 권한체계, 멀티테넌시(동시 여러 업체 서빙), 대상DB에 대한 DDL/SP 생성, 멀티-DBMS(대상DB는 MSSQL 고정) |

## 🏗 진행 내용

- 레거시 소스를 직접 읽고 실행 흐름(ScheduledExecutorService+scheduleAtFixedRate, isTaskRunning 중복차단, JDBC EXEC, HttpURLConnection POST)을 파악 → Quartz+JDBC JobStore 기반 범용 엔진(`ScheduleExecutor`/`ExecutionResult`/`ActionHandler`)으로 일반화
- 백엔드(Spring Boot REST API) / 프론트엔드(React SPA) 분리, JWT stateless 인증, AES-256-GCM 비밀값 암호화
- 스케줄당 대상DB를 N개까지 선택할 수 있도록 N:M 스키마로 확장, 순차 실행+부분실패 허용(`PARTIAL_SUCCESS` 상태 신설)
- cron 문법을 몰라도 되는 구조화 반복주기 입력 UI(`CronBuilder`, 6가지 패턴) 추가
- 보안 리뷰 2라운드(SQL 인젝션, 비밀값 마스킹 실패, JSON 이스케이프 누락, 트랜잭션 경계 등 실제 결함 발견·수정)
- 프론트엔드 디자인 폴리싱
- 실제 배포 가능 인프라가 Tomcat뿐이라는 제약 확인 → WAR 패키징 전환, 프론트 빌드를 백엔드 WAR에 통합하는 단일 빌드 파이프라인, SPA 폴백 라우팅, API 상대경로화까지 전환

아직 손대지 않은 것:

- **실행이력(로그) 테이블** — `ExecutionResult`/`ExecutionResultSink` 경계만 잡아두고 실제 영속화는 미래 라운드(T28)로 미룸
- **실제 운영 Tomcat 배치** — 로컬에서 실제 Tomcat 10.1.55를 다운받아 엔드투엔드까지 검증은 했지만, 회사 인프라의 실제 Tomcat에 올리는 건 아직

## ✅ 결과 및 회고

- **레거시를 "참고"로만 쓰고 바닥부터 새로 설계하려는 유혹을 몇 번이나 막아야 했다.** 리서치 단계에서 AI 에이전트가 레거시를 깊이 안 보고 범용 아키텍처 비교조사부터 시작하길래 중단시키고 다시 지시한 게 가장 처음에 있었던 교정이었다 — "포팅"이라는 말의 의미를 계속 분명히 해야 했다.
- **다른 무관한 프로젝트의 설정을 그대로 베끼는 문제가 두 번 발생했다.** Spring Boot 버전/Lombok 빌드설정이 `ReeL-Trip`(완전히 다른 프로젝트)의 `pom.xml`과 우연히 동일한 걸 발견해서 Maven Central에서 직접 조회해 독립적으로 재확정했다. AI에게 작업을 맡길 때 "어디서 가져왔는지" 검증이 왜 중요한지 체감했다.
- **보안 리뷰를 2라운드 돌린 게 실제로 버그를 잡았다.** SP명 SQL 인젝션, 짧은 비밀값 마스킹 실패, JSON 바디 이스케이프 누락, 트랜잭션 경계 없음 등 — 전부 "동작은 하지만 틀린" 종류의 결함이라 기능 테스트만으론 못 잡았을 것들이다.
- **"범용성"의 범위를 계속 좁혀야 했다.** 처음엔 멀티테넌시(여러 업체를 한 프로세스가 동시 서빙)까지 고려됐는데, 실제 요구는 "재컴파일 없이 재배포"였을 뿐이라 "1프로세스=1배포=1업체" 전제로 단순화했다. 반대로 "대상DB 다중선택"은 실제 필요(한 업체가 여러 지점 DB를 가질 수 있음)라서 범위에 넣었다 — 범용성을 넓힐지 좁힐지는 매번 "실제로 필요한 사용 사례가 있는가"로 판단해야 했다.
- **배포 환경 제약(Tomcat뿐)을 뒤늦게 반영했다.** 설계 초반엔 "백엔드 jar+내장톰캣, 프론트 별도 배포"를 당연하게 가정했는데, 실제로 쓸 수 있는 인프라가 외부 Tomcat뿐이라는 걸 확인하고서야 WAR 전환·단일 배포 통합으로 되돌아갔다. 인프라 제약은 설계 초반에 먼저 확인했어야 했다.

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/01_Tasks|작업 목록]]
- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs|기술 문서]]
- [[01_Projects/08_MINI/01_SchedulerService/04_References|참고 자료]]
- [[Scheduler-Service 개발 과정]]
