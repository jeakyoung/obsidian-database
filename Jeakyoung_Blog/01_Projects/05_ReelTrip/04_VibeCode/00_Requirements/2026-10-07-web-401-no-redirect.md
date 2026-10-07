---
title: 웹 토큰 만료 시 로그인 리다이렉트 누락 버그
date: 2026-10-07
type: 요구사항서
project: ReelTrip
status: 완료
assignee: []
tags: []
---

## 요구사항 정보

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-10-07 |
| **대상 앱** | Web |
| **대상 페이지/화면** | 공통 (`apiRequest`를 쓰는 모든 화면 — 대시보드, 캘린더, 알림, 멤버 등) |
| **작업 유형** | 버그수정 |
| **우선순위** | 높음 |

---

## 현재 상태 (As-Is)

- `apps/web/src/lib/api-client.ts`의 `attemptRefresh()`: `refresh_token`이 없으면(`if (!refreshToken) return null;`) 즉시 `null`을 반환할 뿐, 저장된 세션(`token`/`username`)을 정리하거나 `/auth/login`으로 리다이렉트하지 않음.
- 반면 같은 함수 내 다른 실패 분기(리프레시 API 호출 실패, `success: false` 응답)는 모두 `localStorage` 정리 + `window.location.href = "/auth/login"`을 수행함 — 이 분기만 빠져 있음.
- 백엔드 access token 만료 시간은 30분(`apps/api-spring/.../application.yml` `jwt.expires-in: 1800000`), `refresh_token`은 "자동 로그인" 옵션을 켠 경우에만 저장됨(`apps/web/src/domains/auth/session.ts`).
- 결과적으로 "자동 로그인" 미설정 상태로 30분 이상 머무르면: 화면에 떠 있는 모든 컴포넌트가 각자 독립적으로 만료된 토큰으로 API를 호출 → 전부 401 → 재발급도 안 되고 로그인 페이지로도 안 보내져서 콘솔에 `teamspaces`/`user/profile`/`notifications` 401이 반복적으로 쌓이고 화면은 조용히 깨진 상태로 남음.

---

## 원하는 상태 (To-Be)

- `refresh_token`이 없어 재발급이 불가능한 경우에도, 다른 실패 분기와 동일하게 세션을 정리하고 `/auth/login`으로 리다이렉트한다.

---

## 상세 요구사항

### 기능 요구사항
1. `attemptRefresh()`의 `if (!refreshToken) return null;` 분기를 다른 실패 분기와 동일하게 `localStorage` 정리(`token`/`refresh_token`/`username`) + `/auth/login` 리다이렉트 후 `null` 반환하도록 수정한다.

### 제약 조건
- 범위를 벗어나는 리팩토링(예: 여러 컴포넌트가 각자 토큰을 읽어 중복 호출하는 구조 개선)은 하지 않는다 — 이번엔 리다이렉트 누락 버그만 수정.

---

## 참고 자료

- `apps/web/src/lib/api-client.ts`
- `apps/web/src/domains/auth/session.ts`
- `apps/api-spring/src/main/resources/application.yml`
