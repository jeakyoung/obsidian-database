---
title: Mobile 전역 상태·서버 캐싱 도입
date: 2026-06-02
type: 작업
project: ReelTrip
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# Mobile 전역 상태·서버 캐싱 도입

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-06-02 |
| **대상 시스템** | Mobile |
| **관련 화면·프로그램** | `app/(tabs)/*`, `src/features/*`, `src/hooks/*`, `src/store/*` |

> 지금 README에 있는 Mobile 폴더 구조(`features/`, `hooks/`, `store/`)가 이 커밋 하나로 자리잡음

## 🔍 현상 및 원인

이 시점까지 Mobile의 화면들(`(tabs)/index.tsx` 538줄, `(tabs)/travel.tsx` 600줄, `(tabs)/calendar.tsx` 401줄 등)이 데이터 fetch, 상태 관리, UI 렌더링을 전부 화면 파일 하나에 때려박은 상태였다. 인증 토큰도 각 모달마다 prop으로 일일이 내려주고 있었고, "토스트 알림" 같은 공통 UI도 없었다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 상태 | `store/auth.ts` (Zustand) | token·username·isReady·setAuth·clearAuth·initFromStorage |
| 상태 | `store/toast.ts` (Zustand) | toast 큐 + `toast.success/error/info` 유틸 |
| 서버 상태 | `hooks/useSpaces.ts` 등 (TanStack Query) | `useSpaces`·`useEvents`·`usePlaces`·`useNotifications`·`useProfile` |
| 구조 | `src/features/{home,calendar,travel,profile,auth,recommend,share}/` | 화면별로 `hooks/`(데이터) + `components/`(UI) + 화면 컴포넌트로 3분할 |
| 공통 UI | `src/components/ui/*` | `Button`, `FormInput`, `EmptyState`, `FAB`, `LoadingScreen`, `StatusBadge`, `Toast` 신규 |
| 초기화 | `app/_layout.tsx` | `QueryClientProvider` + `AuthGuard` + `Toast` 통합 |

가장 큰 구조 변화는 "모달에 token을 prop으로 내려주던 방식"을 없앤 것 — 각 모달이 Zustand auth store를 직접 구독하게 바꿔서, 화면 트리를 타고 토큰을 계속 넘겨야 했던 prop drilling이 사라졌다. `(tabs)/index.tsx`가 538줄 → 140줄(`HomeScreen.tsx`)로 줄어든 게 이 리팩토링의 규모를 보여준다.

`ShareHandler`(공유 인텐트로 들어온 URL 처리)도 이번에 독립 feature 폴더로 분리됐다.

## ✅ 검증 및 결과

- [x] 화면 진입 시 TanStack Query로 데이터가 캐시되고, 탭 전환 후 재진입 시 즉시 렌더링되는지 확인
- [x] 토큰 갱신 후 모든 화면/모달이 prop 전달 없이 새 토큰을 즉시 참조하는지 확인
- [x] Toast 알림이 여러 화면에서 공통으로 동작하는지 확인

## 🔗 참고

- 커밋 `a7b5e2a`
- `README.md`의 Mobile 프로젝트 구조 섹션 — 이 커밋 결과물이 그대로 반영됨
