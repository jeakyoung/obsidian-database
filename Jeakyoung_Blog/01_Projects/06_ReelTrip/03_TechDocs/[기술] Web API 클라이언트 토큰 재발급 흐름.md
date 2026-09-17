---
title: Web API 클라이언트 토큰 재발급 흐름
date: 2026-09-17
type: 기술문서
project: ReelTrip
status: 완료
category: 인증
assignee:
  - 안재경
tags: []
---

# Web API 클라이언트 토큰 재발급 흐름

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **대상 시스템** | Web |
| **적용 범위** | 인증 |
| **관련 모듈** | `apps/web/src/lib/api-client.ts` |

> 401 받으면 그냥 로그아웃시키는 게 아니라, refresh token으로 한 번 더 찔러보고 그래도 안 되면 로그인 페이지로 보냄

## 🎯 배경 및 요구사항

Web에서 API 호출은 전부 `apiRequest<T>()` 하나를 거쳐서 나간다. 컴포넌트마다 fetch를 직접 안 쓰고 이 함수를 감싸 쓰는 이유가, 토큰 만료 처리를 한 곳에서만 하기 위해서다. 매 컴포넌트에서 401 처리를 따로 하면 로그아웃 타이밍이 제각각 되고, 특히 화면 하나에서 API를 여러 개 동시에 쏘는 경우(대시보드 진입 시 `listTeamSpaces` + `listNotifications` 같이 나가는 것들) 401이 여러 번 겹쳐 뜨면 refresh 요청도 여러 번 나가는 문제가 있었음.

## 🏗 설계 및 구현

### 흐름

```
apiRequest(path, init, token)
  → fetch 실행
  → 200번대 → 그대로 JSON 반환 (ApiResponse<T>)
  → 401 →
      path 가 /api/auth/refresh 자체면 → 즉시 로그아웃 처리 (무한루프 방지)
      아니면 → attemptRefresh() 호출
          성공 → 새 accessToken 으로 원래 요청 1회 재시도
          실패 → 로그아웃 처리 (localStorage 정리 + /auth/login 이동)
```

### 동시 401 중복 요청 방지

`attemptRefresh()`는 진행 중인 refresh 요청을 모듈 스코프 변수 `refreshPromise`에 들고 있다가, 이미 진행 중이면 새로 요청을 안 만들고 그 promise를 그대로 돌려준다.

```typescript
let refreshPromise: Promise<string | null> | null = null;

async function attemptRefresh(): Promise<string | null> {
  if (refreshPromise) return refreshPromise;
  ...
  refreshPromise = (async () => { ... })();
  try {
    return await refreshPromise;
  } finally {
    refreshPromise = null;
  }
}
```

대시보드 진입 시 `listTeamSpaces`, `listNotifications`가 거의 동시에 나가는데, 토큰이 만료된 상태로 둘 다 401을 받아도 refresh 요청은 딱 한 번만 나간다. 둘 다 같은 promise를 기다렸다가 새 토큰으로 각자 재시도하는 구조.

### ApiResponse 형태

```typescript
{
  success: boolean;
  data: T | null;
  message: string;
  errorCode: string | null;
  timestamp: number;
}
```

401 자체를 자동으로 삼켜버리기 때문에, 화면 쪽 코드는 대부분 `res.success` / `res.errorCode`만 보고 처리하면 된다. 토큰 만료 자체를 신경 쓸 필요가 없다 — [[초대 에러 메시지 분기 처리]]에서 쓴 `errorCode` 분기도 이 위에서 도는 것.

### auto_login 플래그

refresh 성공 시 `auto_login`이 `true`로 저장돼 있으면 새로 내려온 refresh token으로 교체해서 다시 저장한다. 이 플래그가 없으면(=명시적 로그인 유지 안 함) refresh token은 갱신하지 않는다 — 자동 로그인 켜둔 사람만 refresh token이 계속 롤링되는 구조.

## ✅ 검증

- [x] accessToken 만료 후 API 호출 → 자동으로 새 토큰 받아서 원래 요청 재시도되는지 확인
- [x] refresh token까지 만료된 상태에서 호출 → `/auth/login`으로 이동하는지 확인
- [x] 화면 하나에서 API 여러 개 동시 호출 시 refresh 요청이 1번만 나가는지 확인 (네트워크 탭)

## 🔗 참고

- `apps/web/src/lib/api-client.ts`
- [[초대 에러 메시지 분기 처리]]
