---
date: 2026-08-31
title: ReeL-Trip
---

# ReeL-Trip

AI/LLM 기반 학습 프로젝트 (구 NoName). Turborepo 모노레포로 구성.

## 기술 스택

| 영역 | 경로 | 기술 |
|:--|:--|:--|
| **Web FE** | `apps/web` | Next.js 15 (App Router) |
| **Mobile FE** | `apps/mobile` | React Native (Expo ~54, Expo Router v6) |
| **API** | `apps/api-spring` | Spring Boot 3 |

### 공통 규칙

| 항목 | 내용 |
|:--|:--|
| **공유 타입** | `packages/types` |
| **서버 상태 관리** | TanStack Query |
| **클라이언트 전역 상태** | Zustand |
| **Mobile 디자인 토큰** | `src/lib/colors.ts`, `src/lib/styles.ts` |

### 데이터 계층 (`apps/api-spring` 기준)

| 항목 | 내용 |
|:--|:--|
| **DB** | PostgreSQL — Supabase |
| **ORM · 쿼리 매핑** | MyBatis (`mapper-locations: classpath:mapper/**/*.xml`). JPA/Hibernate 아님 |
| **마이그레이션** | Flyway (`classpath:db/migration`) |
| **벡터 검색** | pgvector · OpenAI `text-embedding-3-small` (1536차원) 임베딩을 Postgres 에 저장·검색 |
| **AI 파서** | Gemini (`gemini-2.5-flash`) — URL 파서로 수집한 콘텐츠에서 여행 정보 추출 |
| **커넥션 풀** | HikariCP (pool size 3) |

> [!warning] 커넥션 풀 설정을 건드릴 때
> HikariCP 는 pool size 3, `max-lifetime` 을 짧게 잡아 두었다.
> 유휴 커넥션 5분 타임아웃에 대응한 값이므로, 이 설정을 늘릴 때는
> 끊긴 커넥션을 집어 쓰지 않는지 함께 확인해야 한다.
>
> 설정 주석에 `Neon` 이 남아 있으나 실제 DB 는 Supabase 다. 주석 정리 필요.

> [!note] AI 파서 네이밍이 실제 구현과 안 맞음
> `AiService` 인터페이스 주석과 `ErrorCode.ANTHROPIC_API_KEY_MISSING`엔 "Claude API"라고 남아있지만,
> 실제 구현(`AiServiceImpl.extractTravelInfo`)은 Gemini 키를 체크하고 Gemini로 호출한다.
> Claude → Gemini로 갈아탄 흔적이 이름에만 남은 상태. 자세한 내용은 기술 문서 참고.

> [!note] Web FE 구조
> FSD(Feature-Sliced Design) 구조로 리팩토링 예정이라, 현재 구조에는 깊게 투자하지 않는 방침입니다.

## 문서 분류

- [[01_Projects/05_ReelTrip/01_Tasks|작업 목록]] - 서비스 구동, DB 아키텍처, 더미데이터 실DB 전환, Todo·채팅 기능 구현
- [[01_Projects/05_ReelTrip/02_Docs|프로젝트 문서]] - 프로젝트 개요, 개발 과정
- [[01_Projects/05_ReelTrip/03_TechDocs|기술 문서]] - GitHub 협업, DB 최적화, 환경 구성 가이드, API 인증 흐름, 모노레포 기반 설정
