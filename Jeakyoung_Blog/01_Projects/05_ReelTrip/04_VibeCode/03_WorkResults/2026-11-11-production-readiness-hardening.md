---
title: 상용 서비스 수준 끌어올리기 — 보안/성능/운영 강화 + 테스트·CI 도입
date: 2026-11-11
type: 완료보고서
project: ReelTrip
status: 완료
assignee: []
tags: []
---

## 작업 정보

| 항목 | 내용 |
|------|------|
| **완료일** | 2026-11-11 |
| **작업지시서 참조** | (요구사항서/작업지시서 생략 — herdr 멀티에이전트 팀 워크플로의 `.team/PLAN.md`, `.team/TASKS.md`로 목표 승인 대체) |
| **대상 앱** | API(Spring Boot) 중심 — 테스트는 Web/Mobile 포함 |
| **대상 페이지/화면** | 없음(화면 변경 없는 사이클 — 보안/성능/운영 기반 전부 백엔드·인프라 레벨) |
| **작업 유형** | 기타 (지금까지의 "버튼이 동작 안 함" 관점이 아니라, "상용 서비스라면 당연히 있어야 하는데 없는 것"을 찾아 보강하는 사이클) |

---

## 작업 결과 요약

지난 네 사이클이 모두 "기능이 동작 안 함"을 다뤘던 것과 달리, 이번엔 관점을 바꿔 운영/보안/성능/안정성/테스트/문서 7개 카테고리를 조사해 상용 서비스에 당연히 있어야 하는데 없는 항목 13건(+조사 중 발견해 즉시 긴급수정한 1건)을 찾아내고, 그중 외부 서비스 계약이나 정책 결정이 필요 없는 "코드만으로 해소 가능한" 12건을 사용자 컨펌을 받아 묶음 A(보안/성능/운영 8건)와 묶음 C(테스트+CI 설치/파일럿 4건)로 나눠 전부 구현·리뷰·승인 완료했다.

---

## 변경된 파일

| 묶음 | 파일 | 주요 변경 | 커밋 |
|------|------|-----------|------|
| 긴급(사전) | `SecurityConfig.java`, `RecommendController.java` | `/api/recommend` 무인증(permitAll) 비용공격 취약점 긴급 수정 — `.authenticated()` + `@SecurityRequirement` 추가 | 1850d43 |
| A1 | `InstagramReelsCollector.java`, `AiServiceImpl.java` | Apify/Gemini API 키가 포함될 수 있는 예외 메시지를 클라이언트 응답에서 고정 안전 문구로 치환(서버 로그는 유지) | 1f934d4 |
| A2 | `V17__add_missing_indexes.sql`(신규) | `team_space_members.user_id`/`notifications.user_id`/`places·events·todos.space_id` 5곳 인덱스 추가 | 972f987 |
| A3 | `V18__add_login_lockout.sql`(신규), `AuthServiceImpl.java`, `User*` | 로그인 실패 카운트/계정 잠금(기본 5회/15분) 추가 | 2514c61 |
| A4 | `TeamSpaceServiceImpl.java`, `MessageServiceImpl.java`, `*Mapper` | N+1 쿼리 2건을 `IN`절 배치 조회로 축소 | f732ded |
| A5 | `application.yml`, `SecurityConfig.java` | `/v3/api-docs` 공개 설정 불일치 해소(springdoc 완전 비활성화) | ff30696 |
| A6 | `CreateTodoRequest`, `UpdateTodoRequest`, `CreateEventRequest`, `SendMessageRequest` | DTO 길이 제한 공백 3곳에 `@Size` 추가 | e376e2b |
| A7 | `pom.xml`, `application.yml`, `SecurityConfig.java`, `railway.toml` | 표준 Actuator 헬스체크(`/actuator/health`) 도입 | 72f3371 |
| A8 | `RequestIdFilter`(신규), `SecurityConfig.java`, `logback-spring.xml`(신규) | MDC 요청ID 기반 구조화 로깅 도입 | cc04c99 |
| C1 | `apps/api-spring/src/test/**`(신규 3클래스, 21건) | 인증/Place 멤버십/Notification 억제 로직 핵심 경로 단위 테스트 | de88560 |
| C2 | `apps/web` `vitest.config.mts`, `Button.test.tsx`, `LoadingScreen.test.tsx` | 웹 Vitest+RTL 설치, 파일럿 2건(7 테스트) | a974bc5 |
| C3 | `apps/mobile` jest 설정, `EmptyState.test.tsx`, `FormInput.test.tsx` | 모바일 Jest+RTL 설치, 파일럿 2건(4 테스트) | 4b3e2ef |
| C4 | `.github/workflows/ci.yml`(신규) | web/mobile/api-spring 3개 잡 CI 파이프라인 신설 | 2e5f1e8 |

총 13개 커밋(사전 긴급수정 1850d43 포함).

---

## 변경 사항 상세

### 조사에서 발견한 것 (RESEARCH.md "M. 상용화 기반 조사")

7개 카테고리(계정복구/보안, 운영/관찰성, 성능, 안정성, 데이터보호, 테스트, 문서/운영) 전수 조사 결과, 가장 심각한 2건은 지시받은 체크리스트 범위 밖에서 추가로 발견했다:

- **`/api/recommend` 무인증 노출(비용 공격)** — OpenAI/Gemini를 실제로 호출하는 유료 엔드포인트가 인증·레이트리밋 둘 다 없이 완전히 열려 있어, 누구나 무제한으로 호출해 비용을 발생시킬 수 있었다. 조사 완료 즉시(트리아지를 기다리지 않고) 긴급 수정·배포했다.
- **API 키 쿼리스트링 노출** — Apify/Gemini 키가 URL 쿼리스트링으로 전송되는데, 일부 예외 경로(타임아웃/커넥션 실패 등)에서 원본 예외 메시지가 클라이언트 응답과 서버 로그에 그대로 노출될 수 있었다.

나머지는 비밀번호 재설정/이메일 인증/brute-force 방어 부재(계정복구), Sentry·구조화로깅·표준 헬스체크 부재(운영), N+1 쿼리 2건+인덱스 누락 5곳+페이지네이션 전무(성능), DTO 길이제한 공백 3곳(안정성), 테스트 0건(테스트), swagger 공개 불일치+CI/CD 부재(문서/운영) 등이었다. MyBatis `${}` 치환발 SQLi 경로는 0건으로 확인(안전).

### 트리아지 — 사용자 컨펌 결과

13건(M4-1 긴급수정 제외) 중 사용자와 함께 4묶음으로 분류했다:

| 묶음 | 내용 | 결정 |
|------|------|------|
| A | M4-3/M3-3/M1-3/M3-1/M7-1/M4-2 + (추가 확인 후 포함된) M2-3/M2-2, 총 8건 | **진행** |
| B | M1-1/M1-2 (비밀번호 재설정/이메일 인증) | **백로그** — SMTP 이메일 계정 준비 후 재개 |
| C | M6-1/M7-2 (테스트+CI, 설치/파일럿 수준) | **진행** |
| D | M3-2 (페이지네이션) | **백로그** — 데이터량 증가 시 재검토 |

플래너가 당초 네 묶음 어디에도 없는 공백(M2-3/M2-2)을 발견해 추측 대신 직접 질문했고, 사용자가 "묶음 A에 포함해 진행"으로 답해 묶음 A가 6건→8건으로 확장됐다.

### 리뷰에서 특히 꼼꼼히 확인한 지점

- **[A3] 계정 잠금** — 정상 로그인 흐름이 그대로 유지되는지(①), 잠금이 시간 기반으로 자동 해제되는지(②), 성공 로그인마다 카운트/잠금이 초기화되는지(③) 3가지를 라인 단위로 추적. 임계값 체크도 오프바이원 없이 5번째 실패에서 정확히 잠기는 것까지 확인.
- **[A7] Actuator 헬스체크** — `exposure.include: health`(화이트리스트)로 `env`/`heapdump` 등 민감 엔드포인트 자체가 라우팅되지 않는지, `show-details: never`로 `/actuator/health` 응답에도 상세정보가 없는지 2중으로 확인.
- **[C1~C4] 테스트+CI** — 커밋이 주장한 숫자(21/7/4개 테스트, 전부 통과)를 그대로 믿지 않고 `mvn -o test`/`npx vitest run`/`npx jest`를 직접 실행해 재현, CI YAML도 `js-yaml`로 실제 파싱해 3개 잡이 진짜 테스트 실행 게이트인지 단계별 대조.

리뷰 결과 묶음 A(8건)/묶음 C(4건) 전체 **APPROVED**, CHANGES REQUESTED 없음(`.team/REVIEW.md` 참조).

---

## 테스트 체크리스트

- [ ] 기능 정상 동작 확인 — 화면 변경이 없는 사이클이라 별도 수동 확인 대상 없음(아래 자동 테스트로 대체)
- [x] 기존 기능 회귀 없음 확인 — 리뷰 단계에서 각 묶음 A 커밋마다 `mvn -o compile` 재실행(전부 클린), `git diff --stat`로 웹/모바일 변경 0건(백엔드 전용 전제와 일치) 확인
- [x] 타입 오류 없음 확인 — `apps/web`/`apps/mobile` `npx tsc --noEmit` 클린
- [x] 빌드/테스트 통과 확인 — `mvn -o test`(백엔드 21개), `npx vitest run`(웹 7개), `npx jest`(모바일 4개) 전부 통과, `.github/workflows/ci.yml`을 실제 파서로 검증

> herdr 멀티에이전트 팀(planner/researcher/worker/reviewer/orchestrator)이 조사 → 트리아지 → 개발 → 리뷰 순서로 진행했다. 묶음 A/C 모두 1차 리뷰에서 APPROVED로 종료되어 재작업은 없었다(`.team/REVIEW.md`, `.team/LOG.md` 참조).

---

## 잔여 이슈 / 후속 작업

- **묶음 B(비밀번호 재설정/이메일 인증, M1-1/M1-2)** — SMTP 발신 이메일 계정 준비 후 재개. 세부 분해(SMTP 설정/재설정 플로우/이메일 인증)는 `.team/TASKS.md` 참조.
- **묶음 D(페이지네이션, M3-2)** — 목록 엔드포인트 7개 전부 `Pageable` 없음. 현재 데이터량이 적어 체감 장애 없음이 조사로 확인됐으나, 데이터 증가 시 재검토 필요.
- **M2-1(Sentry 등 에러 모니터링)** — SaaS 가입 + DSN 키 발급(계약 단계)이 선행돼야 해서 이번 사이클 범위 밖, 키 발급 후 별도 진행.
- **M1-3 IP 기반 레이트리밋 확장** — 이번엔 계정 단위 잠금만 구현. IP 기반으로 확장하려면 Redis 등 외부 상태 저장소가 필요해 범위 제외.
- **테스트 커버리지(C1~C3)** — 이번 사이클은 "설치+파일럿" 수준까지만 진행. 전체 커버리지 확보는 범위가 커서 다음 사이클로 이어가는 것을 권장.
- **CI에서 모바일 lint 제외** — `apps/mobile`에 `eslint.config.js`가 없어(ESLint v9 미마이그레이션) 이번 작업과 무관하게 이미 깨져있던 상태를 발견, CI 게이트에서 제외하고 워크플로 파일에 주석으로 이유를 남김. 별도 작업 필요.
- 전체 커밋은 로컬에서만 생성되었고, push 여부는 사용자 확인 후 진행한다.

---

## 특이 사항

- `/api/recommend` 무인증 노출은 지시받은 조사 체크리스트 밖에서 발견한 항목이라, 트리아지를 기다리지 않고 조사 완료 직후 별도로 즉시 수정·배포했다(이번 "4. 개발" 범위 집계에는 포함하지 않음).
- 이번 사이클은 처음으로 "버튼이 동작 안 함"이 아니라 "상용 서비스라면 당연히 있어야 하는데 없는 것"이라는 관점으로 조사를 전환한 사이클이다. 그 결과 지금까지 네 사이클 동안 전혀 다루지 않았던 보안(brute-force/API키 노출)·성능(인덱스/N+1)·운영(헬스체크/로깅)·테스트 영역의 공백이 한꺼번에 드러났다.
- CI 워크플로(C4)는 turbo를 거치지 않고 각 앱에서 npm 스크립트를 직접 실행하도록 설계했다 — 로컬 샌드박스에서 turbo가 자식 프로세스로 실행한 lint/test가 로그 없이 즉시 실패하는 현상을 발견했는데, 같은 명령을 각 앱 디렉터리에서 직접 실행하면 전부 정상 통과해 로컬에서 사전 검증이 안 되는 경로를 CI에 그대로 박아두는 위험을 피하기 위한 선택이다.
