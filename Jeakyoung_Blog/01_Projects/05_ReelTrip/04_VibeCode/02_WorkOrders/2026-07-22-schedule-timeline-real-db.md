---
title: schedule timeline real db
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
| **요구사항 참조** | 실DB 전환 작업 #2 — ScheduleTimeline |
| **대상 앱** | Web |
| **대상 페이지/화면** | `/dashboard` (DashboardScreen > ScheduleTimeline) |
| **작업 유형** | 실DB 전환 |
| **예상 영향 범위** | lib/date.ts, dashboard/DashboardScreen.tsx |

---

## 요구사항 분석 요약

- `DashboardScreen` 내 `ScheduleTimeline` 컴포넌트가 `DUMMY_SCHEDULE` 상수를 직접 참조 중
- #1 작업으로 `selectedSpace.events`에 실 API 데이터가 채워지므로, 이를 `ScheduleTimeline`에 내려주면 됨
- 단, 데이터 구조 차이가 있어 매핑 로직이 필요:

| 항목 | DUMMY_SCHEDULE | TripEvent (실 데이터) |
|------|----------------|----------------------|
| 날짜 단위 | 하루 단위 행 (`date: "08.01"`) | 기간 범위 (`startDate ~ endDate`) |
| 항목 내용 | 세부 활동 문자열 배열 (`items: string[]`) | 이벤트 제목 + 장소 (`title`, `location`) |
| 추가 건수 | 하드코딩 (`extra: number`) | 해당 날짜에 걸친 이벤트 수로 자동 계산 |

- `lib/date.ts`에 날짜 포맷 유틸이 없어 `"YYYY-MM-DD"` → `"MM.DD"` / 한국어 요일 변환 함수 추가 필요

---

## 작업 계획

### 1단계: 날짜 유틸 추가
- [ ] `apps/web/src/lib/date.ts`에 두 함수 추가
  - `formatMonthDay(dateStr: string): string` — `"2026-08-01"` → `"08.01"`
  - `getKoreanDay(dateStr: string): string` — `"2026-08-01"` → `"토"`

### 2단계: ScheduleTimeline 컴포넌트 수정
- [ ] props 추가: `events: TripEvent[]` 수신
- [ ] 내부 로직 변경:
  1. events를 날짜별로 전개 — 각 event의 startDate ~ endDate 범위를 하루씩 펼쳐 `Map<날짜, TripEvent[]>` 생성
  2. 날짜 오름차순 정렬 후 최대 4개 날짜만 표시 (나머지는 "전체 일정 보기" 버튼으로 유도)
  3. 각 날짜 행에서 이벤트를 칩(chip)으로 렌더 — `title` 텍스트 표시, `color`를 칩 왼쪽 dot에 반영
- [ ] `DUMMY_SCHEDULE` 상수 제거
- [ ] events가 없을 때 빈 상태 메시지 처리: `"등록된 일정이 없습니다"`

### 3단계: DashboardInner에서 props 전달
- [ ] `<ScheduleTimeline />` 호출부에 `events={selectedSpace?.events ?? []}` 추가

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `apps/web/src/lib/date.ts` | 수정 | `formatMonthDay()`, `getKoreanDay()` 추가 |
| `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` | 수정 | `DUMMY_SCHEDULE` 제거, `ScheduleTimeline`에 props 추가, 실 events 렌더링 |

---

## 사이드 이펙트 검토

- `lib/date.ts` 추가 함수는 순수 함수로 기존 코드에 영향 없음
- `ScheduleTimeline`은 `DashboardScreen` 내부 컴포넌트이므로 외부 사용처 없음
- `selectedSpace.events`는 #1 작업에서 이미 실 API로 채워지므로 별도 fetch 추가 불필요
- "외 N개 일정 ▾" 버튼은 이번 작업에서 제거 — 실 데이터에서는 날짜별 이벤트를 모두 노출하는 구조로 변경

---

## 확인 필요 사항

- [ ] 하루에 이벤트가 여러 개일 때 모두 칩으로 나열 vs 일부만 노출하고 `+N개` 표시 중 어느 방향?
  - 제안: **모두 노출** (대시보드 요약 화면이므로 건수가 많지 않을 것으로 예상, 추후 개선 여지)

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
