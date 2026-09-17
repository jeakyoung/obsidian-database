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
| **데이터베이스** | PostgreSQL + pgvector *(노트 기준 · 확인 필요)* |

> [!note] Web FE 구조
> FSD(Feature-Sliced Design) 구조로 리팩토링 예정이라, 현재 구조에는 깊게 투자하지 않는 방침입니다.

## 문서 분류

- [[01_Projects/06_ReelTrip/01_Tasks|작업 목록]] - 서비스 구동, DB 아키텍처, 회의 기록
- [[01_Projects/06_ReelTrip/03_TechDocs|기술 문서]] - GitHub 협업, DB 최적화, 환경 구성 가이드
