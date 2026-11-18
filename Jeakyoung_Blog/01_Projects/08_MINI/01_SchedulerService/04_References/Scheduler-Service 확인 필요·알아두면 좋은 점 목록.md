---
title: Scheduler-Service 확인 필요·알아두면 좋은 점 목록
date: 2026-11-18
type: 참고자료
project: SchedulerService
status: 진행중
category: 체크리스트
tags: []
---

# Scheduler-Service 확인 필요·알아두면 좋은 점 목록

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **용도** | 새 기능 작업·배포 전에 먼저 훑어볼 알려진 이슈/미확인 항목 모음. 각 TechDoc/Task/REVIEW.md에 흩어진 항목들의 모음판 |
| **대상 시스템** | Scheduler-Service 전체 |
| **최종 확인일** | 2026-11-18 |

## ⚙️ 환경 및 전제

- 이 환경에는 브라우저 자동화 도구(Playwright/Puppeteer 등)가 없어, UI 조작이 필요한 DoD는 curl 엔드투엔드 + RTL(React Testing Library) 컴포넌트 테스트로 대체 검증했다. 실제 브라우저 화면을 눈으로 본 건 아니므로 필요 시 로컬에서 `npm run dev`로 직접 확인 권장.
- Docker Desktop이 매 세션 시작 시 꺼져 있는 경우가 있어, Testcontainers(MSSQL) 기반 테스트를 돌리기 전에 수동으로 기동해야 할 수 있다.

## 📖 상세 내용

| 구분 | 내용 | 관련 문서 |
|:--|:--|:--|
| 미구현 | 실행이력(로그) 테이블 — `ExecutionResult`/`ExecutionResultSink` 경계만 잡아두고 영속화는 TBD(T28, 별도 라운드) | `.team/TASKS.md` T28 |
| 필수 전제 | `ROOT.war` 배치가 "권장"이 아니라 **필수** — API 호출이 선행 슬래시 경로(origin-relative)라 서브경로 컨텍스트에 배치하면 API가 깨짐(WHATWG URL 실측 확인) | [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Tomcat 단일 WAR 배포 구조]] |
| 전제 | 운영 Tomcat은 **별도 인스턴스**(다른 포트)로 띄우는 걸 전제로 설계됨 — 기존 서비스와 같은 Tomcat의 ROOT를 공유하면 컨텍스트 충돌 | [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.18 Tomcat 배포방안 논의]] |
| 운영금지 | `AUTH_DISABLED`/`VITE_AUTH_DISABLED`는 로컬 개발 전용 — 운영에서 절대 설정하지 말 것(기동 시 WARN 로그로 경고하지만 실수로 켜질 위험은 남아있음) | [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] JWT stateless 인증과 로컬개발 편의기능]] |
| 경계케이스 | 간격반복 cron(분/시간 조합이 정확히 안 맞아떨어지는 경계값)은 구현 시 단위테스트로 검증했지만, 모든 조합을 다 검증한 건 아님 | [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] 반복주기 구조화 입력(CronBuilder)과 Quartz cron 변환]] |
| 개념주의 | `DisplayOutputStore`는 "이력"이 아니라 "최신 1건 캐시"일 뿐 — 프로세스 재시작 시 사라짐, 영속 저장소 아님 | `.team/PLAN.md` §3.3 |
| 확장시 주의 | `target_db_config`는 MSSQL 전용으로 고정(`db_type` 컬럼 없음) — 다른 DBMS 지원이 필요해지면 스키마+`StoredProcedureInvoker` 양쪽 다 손봐야 함 | `.team/PLAN.md` §1/§4.3 |
| 설계 원칙 | 레거시의 실제 운영 IP/계정/API키는 이 레포 어디에도 없음(working tree+전체 git 히스토리 grep 0건, 리뷰에서 재확인) — 새 기능 추가 시에도 이 원칙 유지 필요 | `.team/REVIEW.md` 계획부합 섹션 |

## ⚠️ 주의사항

이 문서는 스냅샷이다 — 각 항목이 실제로 해소되면(예: 실행이력 테이블 설계 완료, 실제 Tomcat에 운영 배치 완료) 해당 TechDoc/Task의 체크박스를 먼저 갱신하고, 이 표는 그 다음에 정리할 것.

## 🔗 참고

- `.team/PLAN.md`/`TASKS.md`/`REVIEW.md` — 코드 기반 설계·리뷰 원본 문서 (Scheduler-Service 레포)
- [[01_Projects/08_MINI/01_SchedulerService/index|Scheduler-Service 프로젝트 개요]]
