---
title: Tomcat 단일 WAR 배포 구조
date: 2026-11-18
type: 기술문서
project: SchedulerService
status: 완료
category: 배포
assignee:
  - 안재경
tags: []
---

# Tomcat 단일 WAR 배포 구조

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | Scheduler-Service 백엔드+프론트엔드 |
| **적용 범위** | 배포 |
| **관련 모듈** | `pom.xml`(war 패키징), `frontend-maven-plugin`, `SpaWebConfig`, `SecurityConfig` |

> 실제 배포 가능한 인프라가 외부 Tomcat뿐이라는 제약이 확인되면서, "백엔드 jar+내장톰캣, 프론트 별도 배포"였던 전제를 깨고 백엔드 WAR 하나에 프론트 빌드 결과물을 통합하는 단일 배포로 전환했다.

## 🎯 배경 및 요구사항

사용자 직접 확인: "활용 가능한 건 톰캣밖에 없다." 프론트엔드 정적 파일을 Tomcat에서 어떻게 서빙할지 두 방식(백엔드 WAR 하나로 합침 vs 각자 별도 WAR) 중, 단일 배포·CORS 불필요라는 장점으로 **백엔드 WAR 하나로 합치는 쪽**을 택했다. 로컬 개발 워크플로(분리 실행)는 그대로 유지해야 한다는 제약도 있었다.

## 🏗 설계 및 구현

### 1. WAR 패키징 전환 + 로컬 워크플로 보존

`pom.xml`을 `war` 패키징으로 바꾸고 `SchedulerServiceApplication`이 `SpringBootServletInitializer`를 extends, `spring-boot-starter-tomcat`을 `provided` 스코프로 명시(외부 Tomcat과의 클래스 충돌 방지). `provided`는 최종 WAR엔 빠지지만 `mvn spring-boot:run`의 실행 classpath에는 여전히 포함되므로 로컬 개발은 그대로 동작한다 — 실제로 돌려서 확인했다.

### 2. Maven이 프론트 빌드까지 수행 (단일 빌드 파이프라인)

`frontend-maven-plugin`으로 Node/npm을 자동 설치해 `npm run build`를 Maven `prepare-package` 단계에 바인딩(처음 계획은 `generate-resources`였지만, 그러면 `mvn test`마다 매번 npm build가 돌아 느려지는 걸 발견해 `prepare-package`로 바꿈 — `test` 단계 이후라 평소 테스트 반복은 영향 없음). `maven-resources-plugin`으로 `frontend/dist/**`를 `target/classes/static/`로 복사(소스 트리 `src/main/resources/static`에는 커밋하지 않음 — 빌드 산출물과 소스 분리).

### 3. SPA 폴백 라우팅

React Router가 다루는 경로(`/schedules` 등)를 새로고침하면 서버가 모르는 경로라 404가 난다. `PathResourceResolver`를 오버라이드해 "요청 리소스가 없으면 `index.html`로 폴백"하도록 구현. `/api/**`는 `RequestMappingHandlerMapping`이 정적 리소스 핸들러보다 먼저 매칭되어 자연히 배제된다.

> [!warning] SecurityConfig가 화면 자체를 막던 버그
> SPA 폴백을 테스트하다가, 기존 `anyRequest().authenticated()`가 `/api/**`뿐 아니라 **정적 자산(index.html/JS/CSS)까지** 로그인을 요구하고 있어서 로그인 페이지 자체를 못 불러오는 구조적 문제를 발견했다. `.requestMatchers("/api/**").authenticated()` + `.anyRequest().permitAll()`로 교정 — 인증 범위를 API로 좁힌 것이 다른 엔드포인트에 영향 없음을 회귀테스트로 확인.

### 4. API 베이스 URL 상대경로화 — ROOT.war가 "권장"이 아니라 "필수"

운영 빌드(`frontend/.env.production`)에서 `VITE_API_BASE_URL`을 빈 값으로 둬서 `/api/...` 같은 **선행 슬래시 경로**로 호출하게 했다.

> [!warning] WHATWG URL 실측으로 드러난 중요한 사실
> PLAN.md는 처음에 "상대경로로 호출하므로 컨텍스트 경로가 무엇이든 동작한다"고 적었는데, 실제로 `new URL('/api/schedules', 'http://host/scheduler-service/index.html')`를 Node로 직접 실행해보니 결과가 항상 `http://host/api/schedules`(origin root)였다 — 페이지가 `/scheduler-service/`에서 서빙돼도 `/scheduler-service/api/schedules`가 되지 않는다. **선행 슬래시 경로는 "컨텍스트 경로 무관"이 아니라 "도메인 무관"만 달성한다.** 즉 **`ROOT.war`로 배치하는 게 선택이 아니라 이 설계의 필수 전제조건**이다. README에도 "권장"이 아니라 "필수"로 명시했다.

이 전제는 "기존에 같은 Tomcat을 쓰는 다른 서비스들과 컨텍스트 경로가 안 꼬이냐"는 우려와 직결됐고, 결국 **별도 Tomcat 인스턴스**(다른 포트)에 ROOT로 배치하는 쪽으로 결정했다.

### 5. 환경변수 공급 — setenv.sh/bat + 시스템 프로퍼티

외부 Tomcat은 `catalina.sh`로 기동되므로, `$CATALINA_HOME/bin/setenv.sh`에 `JAVA_OPTS="-DDB_URL=... -DMASTER_ENCRYPTION_KEY=..."` 형태로 주입한다. Spring Boot가 JVM 시스템 프로퍼티(`-D`)와 OS 환경변수를 똑같이 `${VAR}` 플레이스홀더로 해석하므로 코드 변경이 전혀 필요 없다.

## ✅ 검증

- [x] `mvn spring-boot:run`이 WAR+provided 스코프 상태에서도 로컬 기동됨(회귀)
- [x] Node/npm이 전혀 없는 깨끗한 환경에서 `mvn clean package` 한 번으로 끝까지 성공, WAR 안에 `index.html`+JS/CSS 포함 확인
- [x] 실제 Apache Tomcat 10.1.55(임베디드와 동일 버전)를 로컬에 다운로드해 `ROOT.war`로 배치 → 로그인→스케줄 CRUD→지금실행→삭제까지 엔드투엔드 curl 검증
- [x] 로컬 분리 실행(백엔드 8080+프론트 5173, CORS) 워크플로 회귀 없음 재확인

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/03_Meetings/Scheduler-Service 11.18 Tomcat 배포방안 논의]]
- `.team/PLAN.md` §11, `.team/TASKS.md` T22~T27 (Scheduler-Service 레포)
