---
title: real db migration
date: 2026-08-20
type: 요구사항서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

# 요구사항지시서

> 더미데이터 실DB 전환 — 잔여 항목 일괄 처리

---

## 요구사항 정보

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-08-20 |
| **대상 앱** | Web |
| **대상 페이지/화면** | `/dashboard` (DashboardScreen, AiScreen) |
| **작업 유형** | 실DB 전환 |
| **우선순위** | 높음 |

---

## 현재 상태 (As-Is)

코드베이스 탐색 결과, Web 앱에서 아직 더미데이터를 사용 중인 곳은 3개 영역입니다.

### #1 — AiScreen.tsx `DUMMY_AI_RECS`
- **파일**: `apps/web/src/domains/dashboard/components/AiScreen.tsx` (줄 14-19)
- AI 추천 여행지 섹션이 하드코딩된 3개 객체 배열로 고정
- 구조: `{ id, name, region, emoji, reason }`

### #2 — DashboardScreen.tsx `BookingStatus` 하드코딩 items
- **파일**: `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` (줄 246-251)
- 항공권 / 숙소 / 렌터카 / 액티비티 예약 현황이 하드코딩
- 구조: `{ emoji, label, done, total, status, color }`

### #3 — TravelHeroCard 통계 하드코딩 (`12개`, `4일`, `4개` 등)
- **파일**: `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` (줄 102-106)
- "저장된 장소 12개", "예약 완료 4개" 등이 하드코딩된 숫자

---

## 원하는 상태 (To-Be)

- #1: 실제 저장된 장소 데이터를 기반으로 AI 추천 로직 or 유사 장소 API 연동
- #2: 실 예약 데이터 or 이벤트 데이터 기반으로 예약 현황 표시
- #3: places, events, todos 등 실 API 데이터에서 집계한 숫자 표시

---

## 상세 요구사항

### 기능 요구사항

1. **#1 AiScreen 추천 데이터**
   - 현재 `DUMMY_AI_RECS`는 "비슷한 여행지 (AI 추천)" 섹션에 사용 중
   - Spring API에 AI 추천 엔드포인트가 없는 상태
   - **방향 결정 필요**: A안(저장된 places 기반 추천 흉내), B안(섹션 숨김 또는 "준비 중"), C안(Spring AI 추천 API 신규 구현)

2. **#2 BookingStatus**
   - 현재 예약 상태를 관리하는 Spring API 또는 데이터 모델 존재 여부 확인 필요
   - **방향 결정 필요**: A안(events 중 특정 카테고리로 예약 현황 도출), B안(컴포넌트 숨김), C안(예약 테이블 신규 구현)

3. **#3 TravelHeroCard 통계**
   - "저장된 장소": `listPlaces()` 결과의 `length`로 대체 가능 (이미 fetch 중)
   - "일정": events 날짜 범위로 계산 가능 (이미 fetch 중)
   - "예약 완료": #2 결정에 따라 연동
   - 멤버 수: 이미 실 데이터(`space.members.length`) 사용 중

### UI/UX 요구사항
1. 빈 상태(데이터 없을 때) 처리 필요
2. 로딩 상태 기존 패턴과 동일하게 유지

### 제약 조건
- 요청된 범위만 변경. 불필요한 리팩토링 금지.
- 기존 완료된 작업(events, places, todos fetch)의 코드 패턴 재활용.

---

## 확인 필요 사항

- [ ] #1 AiScreen 추천: A / B / C 중 어떤 방향?
- [ ] #2 BookingStatus: A / B / C 중 어떤 방향?
- [ ] #3 TravelHeroCard 통계: places/events 기반 집계로 진행해도 되는가?

---

## 참고 자료

- 이전 완료된 작업: `docs/results/2026-07-22-*.md`
- 기존 fetch 패턴: `DashboardScreen.tsx` — `listEvents()`, `listPlaces()`, `listTodos()`
