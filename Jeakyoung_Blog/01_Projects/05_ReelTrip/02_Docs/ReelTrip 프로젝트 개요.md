---
title: ReelTrip 프로젝트 개요
date: 2026-09-17
type: 프로젝트문서
project: ReelTrip
status: 진행중
tags: []
---

# ReelTrip 프로젝트 개요

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **프로젝트** | ReelTrip |
| **기간** | 2026-06 ~ 진행중 |
| **역할** | 풀스택 (Web / Mobile / API) |
| **기술 스택** | Next.js 15, React Native(Expo), Spring Boot 3, PostgreSQL |

> AI/LLM 기반 여행지 추천 · 팀 여행 플래닝 서비스. Turborepo 모노레포로 Web/Mobile/API 세 개를 같이 굴린다.

## 🎯 목표 및 범위

여행 일정을 팀 단위로 짜고 공유하는 서비스. 링크(유튜브/인스타 등)를 던지면 파싱해서 장소 후보로 등록하고, 팀스페이스 안에서 일정/장소/할일을 같이 관리하는 게 핵심 플로우다.

| 앱 | 경로 | 기술 |
|:--|:--|:--|
| Web FE | `apps/web` | Next.js 15 (App Router) |
| Mobile FE | `apps/mobile` | React Native (Expo ~54, Expo Router v6) |
| API | `apps/api-spring` | Spring Boot 3 |

공통 규칙:

| 항목 | 내용 |
|:--|:--|
| **공유 타입** | `packages/types` |
| **서버 상태 관리** | TanStack Query |
| **클라이언트 전역 상태** | Zustand |
| **Mobile 디자인 토큰** | `src/lib/colors.ts`, `src/lib/styles.ts` |

데이터 계층(`apps/api-spring` 기준):

| 항목 | 내용 |
|:--|:--|
| **DB** | PostgreSQL (Supabase) |
| **ORM · 쿼리 매핑** | MyBatis — JPA/Hibernate 아님 |
| **마이그레이션** | Flyway |
| **벡터 검색** | pgvector + OpenAI `text-embedding-3-small` (AI 추천용, 아직 검증 중) |
| **커넥션 풀** | HikariCP |

## 🏗 진행 내용

원래 더미데이터로 화면만 붙어 있던 부분들을 실 DB 연동으로 하나씩 바꿔가는 중이다.

- Dashboard 예약 현황(BookingStatus) 하드코딩 → 제거, 저장된 장소 수는 `listPlaces` 결과로 실집계
- 일정(TravelHeroCard 통계) → `listEvents` 기반 실데이터로 교체
- TeamSpace / Todo 패널 → 실 API 연동 완료
- ESLint 도입, 죽은 라우트 정리, 로그인 화면 재구현
- Web API 클라이언트에 401 자동 재발급 흐름 적용 ([[Web API 클라이언트 토큰 재발급 흐름]])

아직 안 끝난 것:

- AiScreen의 "AI 추천" 섹션이 아직 `DUMMY_AI_RECS` 하드코딩 상태 — Spring 쪽에 추천 API가 없어서 방향 결정 필요 (저장된 장소 기반 흉내 낼지 / 섹션을 숨길지 / 진짜 추천 API를 새로 만들지)

## ✅ 결과 및 회고

당장은 더미 걷어내는 작업 위주로 진행 중이고, AI 추천 쪽은 아직 방향이 안 정해진 상태라 남겨둠. Web 쪽은 FSD 구조로 리팩토링할 예정이라 지금 폴더 구조에 깊게 투자하지 않는 방침 유지 중.

## 🔗 참고

- [[01_Projects/05_ReelTrip/01_Tasks|작업 목록]]
- [[01_Projects/05_ReelTrip/03_TechDocs|기술 문서]]
- [[ReelTrip 개발 과정]]
- [[Web API 클라이언트 토큰 재발급 흐름]]
