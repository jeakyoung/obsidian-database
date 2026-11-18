---
title: Scheduler-Service Tomcat 단일WAR 배포 전환 11.17-18
date: 2026-11-18
type: 작업
project: SchedulerService
status: 완료
priority: 매우높음
assignee:
  - 안재경
tags: []
---

# Scheduler-Service Tomcat 단일WAR 배포 전환 11.17-18

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | 본인 — "해당 프로젝트를 배포한다고 쳤을 때, 활용 가능한 건 톰캣밖에 없어" |
| **요청일** | 2026-11-17 ~ 11-18 |
| **대상 시스템** | Scheduler-Service 백엔드/프론트엔드 |
| **관련 화면·프로그램** | TASKS.md T22~T27 전체 |

> 실제 배포 가능한 인프라가 외부 Tomcat뿐이라는 제약에 맞춰 "백엔드 jar+내장톰캣, 프론트 별도배포" 전제를 "Tomcat 단일 WAR" 배포로 전환한 작업.

## 🔍 현상 및 원인

설계 초반엔 jar+내장톰캣(백엔드)/별도 정적서버(프론트) 분리배포를 당연하게 가정했는데, 실제 배포처가 외부 Tomcat뿐이라는 걸 뒤늦게 확인했다. 백엔드 WAR에 프론트 빌드결과를 통합하는 단일배포 방식으로 바꾸기로 결정([[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.18 Tomcat 배포방안 논의]]).

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| T22 | `pom.xml` | war 패키징 전환, `SpringBootServletInitializer`, tomcat `provided` 스코프 |
| T23 | `pom.xml` | `frontend-maven-plugin`으로 Maven이 npm build까지 수행(prepare-package 단계), `maven-resources-plugin`으로 `target/classes/static`에 복사 |
| T24 | `SpaWebConfig`, `SecurityConfig` | SPA 폴백 라우팅 + 정적자산까지 인증 요구하던 버그 수정(`/api/**`만 보호로 좁힘) |
| T25 | `.env.production`, `client.ts` | API 베이스URL 상대경로화, WHATWG URL 실측으로 ROOT.war가 필수 전제임을 확인 |
| T26 | 전체 | 분리실행/통합WAR 두 로컬 워크플로 회귀없음 종합확인(실제 Apache Tomcat 10.1.55로 엔드투엔드) |
| T27 | `README.md` | WAR빌드→Tomcat배치(ROOT.war)→setenv.sh 환경변수→기동 가이드 |

도중에 "기존 서비스들과 ROOT 컨텍스트가 안 꼬이냐"는 우려가 나와, 별도 Tomcat 인스턴스(다른 포트)로 띄우는 쪽으로 결정했고, Vercel+Tomcat 분리배포도 검토했지만 방향을 바꾸지 않기로 했다.

## ✅ 검증 및 결과

- [x] `mvn spring-boot:run`이 WAR 전환 후에도 로컬 기동(회귀 없음)
- [x] Node/npm 없는 환경에서 `mvn clean package` 한 번으로 WAR 생성(프론트 포함) 성공
- [x] 실제 Tomcat 10.1.55에 `ROOT.war` 배치 → 로그인→CRUD→실행→삭제 엔드투엔드 curl 검증
- [x] 로컬 분리실행(CORS 포함) 워크플로 회귀 없음

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Tomcat 단일 WAR 배포 구조]]
- [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.18 Tomcat 배포방안 논의]]
- `.team/PLAN.md` §11, `.team/TASKS.md` T22~T27 (Scheduler-Service 레포)
