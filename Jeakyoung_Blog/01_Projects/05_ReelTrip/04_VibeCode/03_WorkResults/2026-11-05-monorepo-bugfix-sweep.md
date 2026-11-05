---
title: 모노레포 전반 버그 조사 및 수정
date: 2026-11-05
type: 완료보고서
project: ReelTrip
status: 완료
assignee: []
tags: []
---

## 작업 정보

| 항목 | 내용 |
|------|------|
| **완료일** | 2026-11-05 |
| **작업지시서 참조** | (요구사항서/작업지시서 생략 — herdr 멀티에이전트 팀 워크플로의 `.team/PLAN.md`, `.team/TASKS.md`로 목표 승인 대체) |
| **대상 앱** | Web / Mobile / API (공통) |
| **대상 페이지/화면** | 인증(로그인), 장소(Travel), 대시보드 멤버 관리, 홈/캘린더/공유, 팀스페이스, 투두 |
| **작업 유형** | 버그수정 |

---

## 작업 결과 요약

모노레포 전체(apps/web, apps/mobile, apps/api-spring)를 조사해 재현 가능한 버그 4건과 저위험 설계 결함 2건을 찾아 모두 수정했다.

---

## 변경된 파일

| 파일 경로 | 변경 유형 | 주요 변경 내용 |
|-----------|-----------|----------------|
| `apps/mobile/src/lib/api-client.ts` | 수정 | `attemptRefresh()`에서 refreshToken이 없는 분기에 `clearAuth()` 호출 추가 (웹 f1d6d08과 동일 패턴) |
| `apps/api-spring/.../place/controller/PlaceController.java` | 수정 | `PATCH /api/places/{id}` 엔드포인트 신규 추가 |
| `apps/api-spring/.../place/service/PlaceService.java`, `impl/PlaceServiceImpl.java` | 수정 | `update` 메서드 신규 구현 (멤버십 체크 포함) |
| `apps/web/src/domains/travel/components/TravelMapScreen.tsx` | 수정 | `updatePlace(...).catch(() => {})` 제거, 실패 시 로컬 상태 롤백 + 토스트 |
| `apps/mobile/src/features/travel/hooks/useTravelData.ts` | 수정 | 동일 (실패 시 롤백 + 토스트) |
| `apps/mobile/src/features/travel/components/PlaceCorrectSection.tsx` | 수정 | `res.success` 체크 후 실패 시 `onUpdate` 미호출 + 에러 토스트 |
| `apps/web/src/domains/dashboard/components/MemberScreen.tsx` | 수정 | 초대하기/내보내기 버튼에 `onClick` 연결, 성공/실패 인라인 피드백 |
| `apps/mobile/src/store/space.ts` | 생성 | 전역 "현재 스페이스" 선택 상태(zustand store) |
| `apps/mobile/src/features/home/hooks/useHomeData.ts`, `features/calendar/hooks/useCalendarData.ts`, `components/ShareHandler.tsx` | 수정 | `spaces[0]` 고정 참조를 전역 `selectedSpaceId`로 교체 |
| `apps/api-spring/.../teamspace/service/TeamSpaceServiceImpl.java` | 수정 | `removeMember`에 오너 자기제거 방어 추가 |
| `apps/api-spring/.../common/ErrorCode.java` | 수정 | `OWNER_CANNOT_BE_REMOVED` 에러코드 추가 |
| `apps/api-spring/.../todo/service/TodoServiceImpl.java` | 수정 | `update`에서 `dueDate`도 null 체크 후 부분 반영하도록 변경 |

---

## 변경 사항 상세

### 1. 모바일 — refreshToken 없을 때 로그인 리다이렉트 안 됨 (Critical)

**변경 전:**
```ts
const { refreshToken } = useAuthStore.getState();
if (!refreshToken) return null;
```

**변경 후:**
```ts
const { refreshToken } = useAuthStore.getState();
if (!refreshToken) {
  useAuthStore.getState().clearAuth();
  return null;
}
```

**변경 이유:**
- 웹에서는 f1d6d08로 이미 고쳐졌으나 모바일에는 동일 버그가 남아있었다. `clearAuth()`가 호출되지 않으면 만료된 `token`이 store에 그대로 남아 `AuthGuard`(falsy 전환만 감지)가 반응하지 않고, 매 요청마다 401만 반복된다.

### 2. Place 수정/확정 토글이 서버에 저장되지 않음 (Critical, 웹+모바일)

**변경 전:** `PATCH /api/places/{id}`가 백엔드에 전혀 존재하지 않는 상태에서, 프런트는 `updatePlace(...).catch(() => {})`로 에러를 완전히 무시하거나(웹/모바일 토글), `res.success` 체크 없이 바로 로컬 상태를 갱신(모바일 수정 폼)했다.

**변경 후:** 백엔드에 `update` 엔드포인트/서비스를 신규 구현하고, 프런트는 실패 시 로컬 상태를 되돌리고 토스트로 알린다.

**변경 이유:**
- "장소 확정" 토글과 "장소 정보 수정"이 화면상으로는 성공한 것처럼 보이지만 서버에 전혀 반영되지 않아, 새로고침 시 값이 원래대로 돌아가는 문제였다.

### 3. 웹 `/dashboard/member` 초대·내보내기 버튼 미동작 (High)

**변경 전:** 버튼에 `onClick`이 없어 클릭해도 아무 동작도 하지 않았다(`inviteMember`/`removeMember` import조차 없음).

**변경 후:** 두 버튼에 각각 `inviteMember`/`removeMember` 호출을 연결하고 성공/실패 인라인 메시지를 표시한다.

### 4. 모바일 탭 간 "현재 스페이스" 불일치 (Medium)

**변경 전:** Travel 탭은 로컬 `selectedIdx`로 스페이스를 전환할 수 있었지만, Home/Calendar 탭과 공유 수신 화면은 항상 `spaces[0]`(첫 번째 스페이스)만 참조했다.

**변경 후:** `store/space.ts`에 전역 `selectedSpaceId`를 추가해 네 화면이 동일한 값을 공유하도록 변경했다.

**변경 이유:**
- 팀스페이스가 2개 이상인 사용자가 Travel 탭에서 스페이스를 전환해도 Home/Calendar에는 반영되지 않는 데이터 불일치가 있었다.

### 5. 팀스페이스 오너 자기제거 서버 방어 누락 (Medium)

**변경 전:** `removeMember`가 요청자가 오너인지만 확인하고, 제거 대상이 오너 자신인지는 확인하지 않았다.

**변경 후:** 제거 대상이 오너 자신이면 `OWNER_CANNOT_BE_REMOVED` 에러로 거부한다.

**변경 이유:**
- 현재 모바일 UI는 오너에게 제거 버튼을 노출하지 않아 일반적인 사용 흐름에서는 트리거되지 않지만, API를 직접 호출하면 오너 없는 팀스페이스(고아 데이터)가 생성될 수 있었다.

### 6. Todo `dueDate` 부분수정 시 유실 가능 (Low~Medium)

**변경 전:** `priority`/`isDone`은 null 체크 후 부분 반영하지만 `dueDate`는 무조건 덮어써, 요청에 `dueDate`가 없으면 기존 값이 삭제될 수 있었다.

**변경 후:** `dueDate`도 동일한 null 체크 패턴으로 변경.

**변경 이유:**
- 현재 유일한 호출부(모바일 `useTodos.ts`)는 항상 전체 필드를 채워 보내 당장 데이터 손실은 없으나, 서비스 레이어 자체의 설계 결함이라 함께 수정했다.

---

## 테스트 체크리스트

- [ ] 기능 정상 동작 확인 — **미검증** (실제 앱/서버 실행 환경에서 수동 확인 필요)
- [ ] 기존 기능 회귀 없음 확인 — **미검증**
- [ ] 타입 오류 없음 확인 — 미실행
- [ ] 빌드 통과 확인 — 미실행

> 이번 작업은 herdr 멀티에이전트 팀(planner/researcher/worker/reviewer)이 코드 추적 기준으로 조사·구현·리뷰했으며, 리뷰어가 6건 모두 `.team/REVIEW.md`에 APPROVED로 기록했다. 다만 런타임 실행 검증(앱 구동, 서버 기동, dotnet/spring 빌드 등)은 수행하지 않았으므로 사용자 측 실환경 확인이 필요하다.

---

## 잔여 이슈 / 후속 작업

- 아래 항목:
  - "장소 확정" 토글은 여전히 서버에 `confirmed` 상태 컬럼이 없어 설계상 영속화되지 않는다(이번 범위는 에러 무시 제거 + 롤백까지만 — 상태 자체를 영속화할지는 별도 요구사항 필요).
  - 웹 Todo 위젯의 `handleDelete`가 `res.success` 체크 없이 로컬에서 바로 삭제 처리하는 경미한 패턴(조사 중 발견, D3 보조)은 이번 범위에 포함하지 않음.
  - 모바일에 팀스페이스 수정/삭제 기능이 없는 것(기능 격차)과 `PlaceSimilarSection`/`onConsent`의 미구현 API는 버그가 아닌 기능 격차/미구현으로 분류해 이번 수정 대상에서 제외함.
  - 전체 커밋은 로컬에만 생성했고 원격 push는 하지 않음.

---

## 특이 사항

- herdr 멀티에이전트 팀 워크플로(`.team/PLAN.md`, `RESEARCH.md`, `TASKS.md`, `REVIEW.md`, `LOG.md`)로 조사 → 우선순위 확정 → 수정 → 리뷰까지 전 과정을 진행했고, 각 수정 항목을 개별 커밋(da7f827, 3aa39d1, 1cdf00a, c90b86b, 16c6299, fa49378)으로 분리했다.
- ReelTrip CLAUDE.md의 0~2단계(요구사항서/작업지시서/컨펌)는 생략하고 `.team/` 체크리스트로 대체했다 — PLAN.md의 Open Questions에 그 판단 근거를 기록해 두었다.
