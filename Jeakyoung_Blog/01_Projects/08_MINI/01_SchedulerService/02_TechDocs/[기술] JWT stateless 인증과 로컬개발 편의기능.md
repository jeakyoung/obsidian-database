---
title: JWT stateless 인증과 로컬개발 편의기능
date: 2026-11-18
type: 기술문서
project: SchedulerService
status: 완료
category: 인증·개발편의
assignee:
  - 안재경
tags: []
---

# JWT stateless 인증과 로컬개발 편의기능

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | Scheduler-Service 백엔드/프론트엔드 |
| **적용 범위** | 인증 · 로컬 개발환경 |
| **관련 모듈** | `JwtTokenService`, `JwtAuthenticationFilter`, `SecurityConfig`, `AUTH_DISABLED`/`VITE_AUTH_DISABLED`, H2 fallback |

> 레거시엔 인증 자체가 없었다. React SPA가 백엔드와 다른 오리진이라는 전제에서 세션 쿠키 대신 stateless JWT를 택했고, 로컬 테스트를 쉽게 하려고 인증/DB 둘 다 opt-in으로 끌 수 있는 편의기능을 추가했다.

## 🎯 배경 및 요구사항

사용자 직접 지시: 인증 방식을 토큰(JWT) 기반으로 확정 — 세션 쿠키 방식은 SPA가 다른 오리진일 때 `SameSite=None+Secure+CORS Allow-Credentials+CSRF`까지 다 갖춰야 하는데, 단일 관리자 역할의 내부 어드민 도구 규모에는 불필요한 복잡도라는 판단. 이후 로컬 테스트 편의를 위해 "로그인을 일단 건너뛸 수 있게"/"DB 설정 없이도 구동"이 요청됐다.

## 🏗 설계 및 구현

### JWT stateless 인증

- `SecurityConfig`: `SessionCreationPolicy.STATELESS` + CSRF 비활성(쿠키 자체가 없으므로), `/api/auth/login`·`/api/health`만 `permitAll`, 나머지 `anyRequest().authenticated()`.
- 서명키(`JWT_SIGNING_KEY`)와 비밀값 암호화 마스터키(`MASTER_ENCRYPTION_KEY`)를 **별도 값**으로 분리(서명키/암호화키 혼용 금지 원칙).
- 최초 기동 시 관리자 계정이 0건이고 `INITIAL_ADMIN_USERNAME`/`PASSWORD`가 설정돼 있으면 1회 시드(BCrypt) — 레거시엔 없던 완전 신규 보호.

> [!warning] 기본 403 대신 401이 필요했던 이유
> `exceptionHandling(...authenticationEntryPoint(...))`를 명시하지 않으면 Spring Security가(formLogin/httpBasic 둘 다 비활성이라) 기본값으로 `Http403ForbiddenEntryPoint`를 써서 미인증 요청이 401이 아니라 403으로 나간다. `HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)`를 명시해서 교정.

### 로컬 개발 편의기능 — AUTH_DISABLED / H2 fallback

| 기능 | 환경변수 | 동작 |
|:--|:--|:--|
| 인증 건너뛰기(백엔드) | `AUTH_DISABLED`(기본 false) | true면 `anyRequest().permitAll()` + JWT 필터 자체를 체인에 안 넣음. 기동 시 WARN 로그로 경고 |
| 인증 건너뛰기(프론트) | `VITE_AUTH_DISABLED`(기본 false) | true면 `AuthContext`가 실제 로그인 없이 더미 유저로 즉시 채워져 `ProtectedRoute`가 리다이렉트 안 함. 네비게이션 바에 경고 배지 표시 |
| 메타DB 없이 기동 | `DB_URL` 미설정 | H2 파일 DB(`./data/scheduler-meta`)로 자동 fallback, Flyway가 H2용 마이그레이션(V1/V2)을 따로 적용 |

- 두 플래그 모두 **opt-in, 기본값은 기존 안전한 동작 유지** — AUTH_DISABLED/DB_URL 둘 다 명시적으로 켜야만 변경된다.
- **백엔드와 프론트는 서로 독립된 게이트**다 — 백엔드만 `AUTH_DISABLED=true`로 띄워도 프론트는 여전히 로그인 화면만 보여준다(클라이언트 사이드 라우트 가드가 서버 설정을 모름). 둘 다 켜야 로그인 없이 화면까지 뚫린다.

> [!warning] 테스트 격리 결함 — 호스트 환경변수가 테스트에 영향
> 로컬 쉘에 `AUTH_DISABLED=true`를 export해둔 채 `mvn test`를 돌리면, 이 값이 테스트 JVM에도 전달돼 "기본값(인증 활성화)에서 보호가 되는지" 검증하는 테스트가 실패했다. `@TestPropertySource(properties = "app.auth.disabled=false")`로 해당 테스트 클래스를 호스트 환경변수와 무관하게 고정.

> [!warning] H2 전환 중 드러난 벤더종속 SQL 버그
> H2로 전환하면서 `WHERE enabled = 1`(정수 리터럴, H2의 엄격한 BOOLEAN 타입과 비교 불가)과 `SYSUTCDATETIME()`(SQL Server 전용 함수) 2건이 리포지토리에 하드코딩돼 있던 걸 발견 — 바운드 파라미터/애플리케이션 시계 기준으로 교정해 두 DB 모두 동일하게 동작하게 했다.

## ✅ 검증

- [x] `AUTH_DISABLED` 설정된 채로도/안 된 채로도 전체 테스트 그린(100/100)
- [x] 인증 없이 `/api/**` 호출 시 401(403 아님), 로그인 후 정상 호출
- [x] `DB_URL` 미설정 시 H2로 자동 기동, Flyway H2 마이그레이션 성공, Quartz 정상 기동
- [x] H2/SQL Server 양쪽에서 동일하게 동작(벤더종속 SQL 수정 후 재확인)

## 🔗 참고

- [[01_Projects/08_MINI/01_SchedulerService/02_TechDocs/[기술] Tomcat 단일 WAR 배포 구조]]
- `.team/LOG.md` T11/H2 fallback/AUTH_DISABLED 섹션 (Scheduler-Service 레포)
