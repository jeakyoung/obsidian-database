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
| **DB** | PostgreSQL — Neon (서버리스) |
| **ORM · 쿼리 매핑** | MyBatis (`mapper-locations: classpath:mapper/**/*.xml`). JPA/Hibernate 아님 |
| **마이그레이션** | Flyway (`classpath:db/migration`) |
| **벡터 검색** | pgvector · OpenAI `text-embedding-3-small` (1536차원) 임베딩을 Postgres 에 저장·검색 |
| **커넥션 풀** | HikariCP (pool size 3) |

> [!warning] Neon 커넥션 타임아웃
> Neon 은 유휴 커넥션을 5분 뒤 끊는다. HikariCP `max-lifetime` 을 그보다 짧게 잡아 두어야
> 끊긴 커넥션을 집어 쓰는 일이 없다. pool size 를 3 으로 작게 잡은 것도 같은 이유다.

> [!note] Web FE 구조
> FSD(Feature-Sliced Design) 구조로 리팩토링 예정이라, 현재 구조에는 깊게 투자하지 않는 방침입니다.

## 문서 분류

- [[01_Projects/06_ReelTrip/01_Tasks|작업 목록]] - 서비스 구동, DB 아키텍처, 회의 기록
- [[01_Projects/06_ReelTrip/03_TechDocs|기술 문서]] - GitHub 협업, DB 최적화, 환경 구성 가이드
