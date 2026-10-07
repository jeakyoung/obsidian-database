---
title: 웹 토큰 만료 시 로그인 리다이렉트 누락 버그
date: 2026-10-07
type: 완료보고서
project: ReelTrip
status: 완료
assignee: []
tags: []
---

## 작업 정보

| 항목 | 내용 |
|------|------|
| **완료일** | 2026-10-07 |
| **작업지시서 참조** | [[Jeakyoung_Blog/01_Projects/05_ReelTrip/04_VibeCode/02_WorkOrders/2026-10-07-web-401-no-redirect]] |
| **대상 앱** | Web |
| **대상 페이지/화면** | 공통 (`apiRequest` 사용 전체) |
| **작업 유형** | 버그수정 |

---

## 작업 결과 요약

`attemptRefresh()`에서 `refresh_token`이 없어 재발급이 불가능할 때 세션 정리/로그인 리다이렉트를 하지 않던 분기를, 다른 실패 분기와 동일하게 처리하도록 수정했다.

---

## 변경된 파일

| 파일 경로 | 변경 유형 | 주요 변경 내용 |
|-----------|-----------|----------------|
| `apps/web/src/lib/api-client.ts` | 수정 | `attemptRefresh()`의 `if (!refreshToken) return null;` 분기에 `localStorage` 정리 + `/auth/login` 리다이렉트 추가 |

---

## 변경 사항 상세

### `attemptRefresh()` (`apps/web/src/lib/api-client.ts`)

**변경 전:**
```ts
const refreshToken = localStorage.getItem("refresh_token");
if (!refreshToken) return null;
```

**변경 후:**
```ts
const refreshToken = localStorage.getItem("refresh_token");
if (!refreshToken) {
  localStorage.removeItem("token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("username");
  window.location.href = "/auth/login";
  return null;
}
```

**변경 이유:**
- 백엔드 access token 만료 시간이 30분(`apps/api-spring/.../application.yml` `jwt.expires-in: 1800000`)인데, "자동 로그인"을 켜지 않으면 `refresh_token`이 저장되지 않는다(`session.ts`). 이 상태로 30분을 넘기면 화면에 떠 있는 모든 컴포넌트(대시보드/캘린더/알림/멤버 등)가 각자 독립적으로 만료된 토큰으로 API를 호출해 전부 401이 나는데, 재발급도 안 되고 로그인 페이지로도 안 보내져서 콘솔에 `teamspaces`/`user/profile`/`notifications` 401이 반복적으로 쌓이고 화면은 조용히 깨진 채로 남아 있었다.
- 같은 함수의 다른 두 실패 분기(재발급 API 호출 실패, 응답 `success: false`)는 이미 세션 정리 + 리다이렉트를 하고 있어, 누락된 분기만 동일하게 맞췄다.

---

## 테스트 체크리스트

- [x] 타입 오류 없음 확인 — `npx tsc --noEmit` 에러 없음
- [ ] 기능 정상 동작 확인 — **미검증** (브라우저에서 만료 토큰 + refresh_token 없는 상태 재현 필요)
- [ ] 기존 기능 회귀 없음 확인 — **미검증**
- [ ] 빌드 통과 확인 — 미실행

---

## 잔여 이슈 / 후속 작업

- 아래 항목:
  - 여러 컴포넌트가 각자 `localStorage`에서 토큰을 읽어 독립적으로 동일 API(`teamspaces` 등)를 중복 호출하는 구조는 이번 범위에서 다루지 않음 — 토큰/세션을 한 곳에서 관리하는 구조로 개선할지는 별도 요구사항으로 검토 필요.
  - 실제 브라우저에서 토큰 만료 + 자동 로그인 미설정 상태를 재현해 `/auth/login` 리다이렉트가 정상 동작하는지 사용자 측 수동 확인 필요.

---

## 특이 사항

- 모바일 APK 빌드(`eas build --platform android --profile preview`)는 이 작업과 별개로 백그라운드에서 계속 대기열(IN_QUEUE) 중.
