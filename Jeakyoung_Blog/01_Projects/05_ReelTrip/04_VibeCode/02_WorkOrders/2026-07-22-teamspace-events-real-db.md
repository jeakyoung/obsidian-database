---
title: teamspace events real db
date: 2026-07-22
type: 작업지시서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

# 작업지시서

> Claude가 요구사항을 분석해 작성하는 문서입니다.
> 사용자 컨펌 후 작업이 시작됩니다.

---

## 작업 개요

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-07-22 |
| **요구사항 참조** | 실DB 전환 작업 #1 — TeamSpace events |
| **대상 앱** | Web |
| **대상 페이지/화면** | `/dashboard` (DashboardScreen) |
| **작업 유형** | 실DB 전환 |
| **예상 영향 범위** | teamspace/mock.ts, teamspace/mappers.ts, dashboard/DashboardScreen.tsx |

---

## 요구사항 분석 요약

- `apps/web/src/domains/teamspace/mock.ts`의 `MOCK_TEAM_SPACES`는 현재 어디에도 import되지 않는 dead code
- 진짜 문제는 `toTeamSpace()` 매퍼가 `events: []`로 하드코딩되어 있어 실 API에서 받아온 팀스페이스에 이벤트가 항상 비어있는 것
- `DashboardScreen`의 `TravelHeroCard`는 `space.events[0].startDate`로 D-day와 여행 날짜를 계산하는데, events가 없어 "D-12", "2026.08.01 (토) ~ 08.04 (화) · 3박 4일" 등의 하드코딩 fallback이 노출되는 상태
- `apps/web/src/domains/event/api.ts`에 `listEvents(spaceId, month, token)` 함수가 이미 존재하므로 연동만 하면 됨

---

## 작업 계획

### 1단계: dead code 제거
- [ ] `apps/web/src/domains/teamspace/mock.ts` 파일 삭제

### 2단계: Event 매퍼 추가
- [ ] `apps/web/src/domains/teamspace/mappers.ts`에 `toTripEvent(res: EventResponse): TripEvent` 함수 추가
  - `EventResponse.id` → `String(id)`
  - `EventResponse.title` → `title`
  - `EventResponse.startDate` → `startDate`
  - `EventResponse.endDate` → `endDate`
  - `EventResponse.location ?? ""` → `location`
  - `EventResponse.color` → `color`

### 3단계: DashboardScreen에 events 페치 연동
- [ ] `DashboardScreen`에 `listEvents` import 추가
- [ ] `spaces` state에 events 포함시키는 흐름 추가:
  - 팀스페이스 목록 로드 후, 선택된 space의 events를 `listEvents(spaceId, null, token)`으로 별도 fetch
  - 결과를 해당 space의 `events` 필드에 merge하여 state 업데이트
- [ ] 사이드바에서 다른 space로 전환 시(`setSelectedSpaceId`) events를 다시 fetch하도록 `useEffect` 의존성 추가
  - 이미 events를 로드한 space는 재요청 없이 캐시 사용 (단순 `Map` 또는 state object로 관리)

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `apps/web/src/domains/teamspace/mock.ts` | **삭제** | dead code, 미사용 |
| `apps/web/src/domains/teamspace/mappers.ts` | 수정 | `toTripEvent()` 매퍼 추가 |
| `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` | 수정 | 선택 space의 events를 실 API로 fetch, space 전환 시 재fetch |

---

## 사이드 이펙트 검토

- `MOCK_TEAM_SPACES`는 현재 import되는 곳이 없으므로 삭제 시 빌드 오류 없음
- `TravelHeroCard`의 하드코딩 fallback 문자열("D-12", "2026.08.01 (토) ~ 08.04 (화)") 은 events가 실제로 채워지면 자연스럽게 사라짐 — 별도 수정 불필요
- events 페치는 선택된 space에 대해서만 수행하므로 초기 로딩 부하 최소화
- `ScheduleTimeline` / `AiRecommendSection` 의 DUMMY 데이터는 이번 작업 범위 **외** (다음 회차)

---

## 확인 필요 사항

- [ ] events를 space마다 캐시할지, 매 전환 시 항상 재요청할지?
  - 제안: 단순하게 **매 전환 시 재요청** (캐시 복잡도 없이 진행, 추후 TanStack Query로 교체 예정이므로)

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
