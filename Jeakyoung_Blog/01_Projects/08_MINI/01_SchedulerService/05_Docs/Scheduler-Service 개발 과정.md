---
title: Scheduler-Service 개발 과정
date: 2026-11-18
type: 프로젝트문서
project: SchedulerService
status: 진행중
tags: []
---

# Scheduler-Service 개발 과정

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **프로젝트** | Scheduler-Service |
| **기간** | 2026-11-13 ~ 진행중 |
| **역할** | 설계·구현·리뷰·배포전환 전체 |
| **기술 스택** | Java 17, Spring Boot 3.5.16, Quartz, React, SQL Server/H2, Tomcat |

> git 로그를 순서대로 다시 훑으며, 실제로 어떤 순서로 왜 그렇게 바뀌어왔는지 정리한 문서. [[Scheduler-Service 프로젝트 개요]]가 "지금 상태" 스냅샷이라면 이건 "어쩌다 지금 상태가 됐는지" 쪽.

## 🎯 목표 및 범위

Herdr 멀티에이전트(researcher/planner/worker/reviewer)를 orchestrator로서 직접 지시하며, 레거시 알림 스케줄러의 실행 흐름을 범용 스케줄링 엔진으로 포팅해나간 과정을 남긴다.

## 🏗 진행 내용

### 1. 리서치 방향 교정 — "포팅"의 의미 확정 (2026-11-13)

리서치 에이전트가 레거시 코드를 깊이 안 보고 범용 아키텍처(Quartz 등) 비교조사부터 시작해서 중단시키고 재지시했다. 목표는 "바닥부터 새 아키텍처"가 아니라 레거시의 `ScheduledExecutorService` 등록 패턴+Task 실행 흐름(SP 호출→결과가공→FCM 발송)을 그대로 포팅하는 것으로 명확히 했다. 자세한 내용은 [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.13 레거시 포팅 방향 교정]].

### 2. 초기 스캐폴딩 + 설계 확정 (`5709e96` ~ `af31bde`, 2026-11-13)

researcher가 Quartz+JDBC JobStore(동적 스케줄)와 2계층 비밀값 주입(부트스트랩 env var/운영값 관리자 웹)을 추천, planner가 PLAN.md/TASKS.md(T1~T14)로 구체화. worker가 `589ee23`(T1 Maven 스캐폴딩)부터 `af31bde`(T10 대상DB/자격증명 API)까지 백엔드 코어를 순서대로 구현 — 메타DB 마이그레이션(`b5d79ee`), 도메인·Repository(`e08d047`), AES-256-GCM 암복호화(`48632cd`), 실행엔진 코어(`ac76889`), Quartz 동적등록(`5abef79`), 스케줄 CRUD API(`56ea47b`).

### 3. 아키텍처 교정 — 백엔드/프론트 분리, React, Spring Boot 버전 재검증 (2026-11-13)

T1에서 생성된 `pom.xml`의 Spring Boot 버전(3.3.5)과 Lombok 빌드설정이 전혀 무관한 다른 프로젝트 `ReeL-Trip`의 설정과 완전히 동일한 것을 발견 — worker가 독립적으로 버전을 판단하지 않고 베낀 것으로 확인. 이어서 "관리자 화면을 Thymeleaf로 같은 Java 앱에 넣을지, 프론트엔드 언어가 뭔지" 질문이 나와 백엔드(REST API 전용)/프론트(React SPA) 완전 분리로 결정, 인증은 JWT(stateless, 세션 쿠키 아님)로 확정. `a8d7841`(T1 재작업: backend/ 분리+thymeleaf 제거+Spring Boot 3.5.16 독립 확정, Maven Central 메타데이터로 직접 조회)부터 다시 진행. 자세한 내용은 [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.13 아키텍처 교정]].

### 4. 기능범위 1차 완성 — T11~T14 (`abc294a` ~ `643b01c`, 2026-11-13~16)

JWT 인증(`abc294a`), React 8개 화면(`233ce5a`), 비밀값 최종점검(`747f2f1`), 레거시 3패턴 회귀테스트(`643b01c`)로 TASKS.md T1~T14 완료. 중간에 "실행이력 저장/다운스트림 2모드/즉시실행/SP파라미터화/대량결과 저장범위" 6가지를 질문받아 확정(실행이력은 TBD로 보류, 다운스트림은 API_CALL/DISPLAY_ONLY 둘 다 지원, 즉시실행 포함, SP 파라미터화 지원, "백업서버가 아니라 감시서버" 원칙). 자세한 내용은 [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.13 기능범위 2차 교정]].

### 5. 1차 보안 리뷰 대응 (`02fee04` ~ `423b99f` 전, 2026-11-16)

reviewer가 SP명 SQL 인젝션(M1)·짧은 비밀값 마스킹 실패(M2)·JSON 이스케이프 누락(N1)·run-now 과거결과 혼입(N3)·cron 문서공백(N2)을 지적, 전부 수정(`02fee04`/`9298c10`/`e113b68`/`30537d4`/`c4479aa`). 같은 날 로컬 테스트 편의를 위해 `AUTH_DISABLED`(`572003d`)/`VITE_AUTH_DISABLED`(`a60f888`)와 H2 메타DB fallback(`d4355b5`)도 추가 — 이 과정에서 테스트가 호스트 환경변수에 의존하던 격리 결함(`473a931`)도 같이 발견해 고쳤다.

### 6. 대규모 기능 확장 — 반복주기UI·대상DB다중선택·업체별모아보기 (`f8aa871` ~ `194daac`, 2026-11-16~17)

사용자 직접 요청으로 3가지 큰 기능이 추가됐다: (1) cron 텍스트 입력 대신 년/월/일/시/분 구조화 입력 → cron 변환, (2) 스케줄당 대상DB를 N개까지 선택해 전부 호출(기존 1:1 FK를 N:M으로 전환), (3) 실행결과를 대상DB별로 묶어보기. `f8aa871`(설계)부터 `55dc772`~`194daac`(T15~T21: 마이그레이션→도메인/엔진→API→CronBuilder→멀티셀렉트+그룹뷰→회귀테스트) 순서로 구현. 이 과정에서 `ExecutionResult`에 `PARTIAL_SUCCESS` 상태가 신설되고 `ScheduleExecutor`가 대상DB를 순차 순회하며 부분실패를 허용하도록 재작성됐다. 자세한 내용은 [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.17 대상DB 다중선택 기능요청]].

### 7. 2차 보안 리뷰 대응 + 디자인 폴리싱 (`49d4c1b` ~ `69fb333`, 2026-11-17)

reviewer 2차 리뷰에서 1차 때 지적한 M1/M2는 재발하지 않았음을 확인했지만, 신규 결함(`targetDbConfigIds` 중복id→500(M4), 트랜잭션 경계 없음(N4), 중복조회(N5))을 발견 — 전부 수정(`93be02d`/`aef01fd`/`57d9b03`). 이어서 프론트엔드 전체 디자인 폴리싱(디자인 토큰 통일, 버튼 위계, 빈상태, 접근성 기본)을 진행(`69fb333`).

### 8. Tomcat 단일 WAR 배포 전환 (`c16157a` ~ `423b99f`, 2026-11-17~18)

실제 배포 가능한 인프라가 외부 Tomcat뿐이라는 제약을 확인하면서, "백엔드 jar+내장톰캣, 프론트 별도배포" 전제를 "Tomcat 단일 WAR"로 전환해야 했다. WAR 패키징(`5ce97b5`), Maven이 프론트 빌드까지 수행하는 통합 빌드 파이프라인(`e0d8cac`), SPA 폴백 라우팅(`f3e1596` — 이 과정에서 기존 보안설정이 정적 자산까지 로그인 요구로 막던 버그를 발견해 같이 고쳤다), API 베이스URL 상대경로화(`c24d56a` — WHATWG URL 해석 실측으로 "ROOT.war 배치가 선택이 아니라 필수 전제조건"임을 확인), 로컬 워크플로 회귀확인(`26a14fc` — 실제 Apache Tomcat 10.1.55를 다운받아 로그인→CRUD→실행까지 엔드투엔드 검증), README 배포가이드(`423b99f`)까지 완료. 도중에 "ROOT.war가 기존 서비스들과 컨텍스트 경로가 안 꼬이냐"는 우려가 나와, 별도 Tomcat 인스턴스(다른 포트)로 띄우는 쪽으로 결정했고 Vercel 분리배포도 검토했지만 기각했다. 자세한 내용은 [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.18 Tomcat 배포방안 논의]].

## ✅ 결과 및 회고

- **"포팅"의 범위를 몇 번이나 다시 확인해야 했다.** 리서치 단계, 설계 단계 모두에서 AI 에이전트가 "더 좋은 범용 아키텍처"로 넘어가려는 경향이 있었고, 그때마다 "레거시 실행 흐름을 그대로 가져간다"는 원칙으로 되돌려야 했다.
- **다른 프로젝트 설정을 그대로 베끼는 문제가 눈에 보이는 형태(버전 숫자 일치)로 드러난 게 다행이었다.** Maven Central 메타데이터를 직접 조회하게 하는 것처럼, "어디서 가져왔는지 검증 가능한 방법"을 지시에 포함시키는 게 중요했다.
- **보안 리뷰를 구현 완료 시점마다(1차 T14 후, 2차 T21 후) 두 번 돌린 게 실제로 효과가 있었다.** 두 라운드 모두 blocking은 없었지만 매번 Major 1~2건을 실제로 잡아냈다 — "기능이 동작한다"와 "안전하게 동작한다"는 다른 질문이라는 걸 체감했다.
- **인프라 제약(Tomcat뿐)을 설계 초반에 확인했어야 했다.** "jar+내장톰캣"을 기본값으로 가정하고 한참 진행한 뒤에야 실제 배포환경을 묻게 됐고, 그래서 WAR 전환이라는 되돌아가는 작업이 생겼다. 다음엔 "이걸 실제로 어디에 올릴 건지"를 설계 맨 처음에 물어봐야겠다.

## 🔗 참고

- [[Scheduler-Service 프로젝트 개요]]
- [[01_Projects/08_MINI/01_SchedulerService/01_Tasks|작업 목록]]
- `git log --reverse -- .` (Scheduler-Service 레포 전체 커밋, 60개+)
