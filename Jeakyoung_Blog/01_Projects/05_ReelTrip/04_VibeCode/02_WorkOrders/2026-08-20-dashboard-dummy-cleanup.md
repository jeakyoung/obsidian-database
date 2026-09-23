---
title: dashboard dummy cleanup
date: 2026-08-20
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
| **작성일** | 2026-08-20 |
| **요구사항 참조** | 2026-08-20-real-db-migration.md |
| **대상 앱** | Web |
| **대상 페이지/화면** | `/dashboard` (DashboardScreen) |
| **작업 유형** | 실DB 전환 + 더미 제거 |
| **예상 영향 범위** | `DashboardScreen.tsx` 단일 파일 |

---

## 요구사항 분석 요약

- `BookingStatus` 컴포넌트 — 예약 로직은 이 서비스 범위 밖이므로 제거
- `TravelHeroCard` 통계 수치 — 이미 fetch 중인 `places` / `space.events` 실 데이터로 교체
- `AiScreen DUMMY_AI_RECS` — 현상 유지 (이번 작업 범위 외)

---

## 작업 계획

### 1단계 — BookingStatus 제거

- [ ] `BookingStatus` 함수 컴포넌트 전체 삭제 (줄 245-271)
- [ ] 렌더 영역에서 `<BookingStatus />` 호출 제거 (줄 689)
- [ ] `<MemberStatus>` 가 단독으로 flex row를 차지하도록 레이아웃 정리 (줄 687-690)

### 2단계 — TravelHeroCard 통계 실 데이터 교체

현재 하드코딩 (줄 102-106):
```
{ icon: "📍", count: "12개",  label: "저장된 장소" }
{ icon: "📅", count: "4일",   label: "일정"        }
{ icon: "👥", count: `${space.members.length}명`, label: "참여 멤버" }  ← 이미 실 데이터
{ icon: "✅", count: "4개",   label: "예약 완료"   }
```

변경 후:
```
{ icon: "📍", count: `${placesCount}개`, label: "저장된 장소" }   ← places.length
{ icon: "📅", count: `${tripDays}일`,   label: "일정"        }   ← events 기간 계산
{ icon: "👥", count: `${space.members.length}명`, label: "참여 멤버" }
```
- "예약 완료" 항목 제거 (BookingStatus 제거와 일관성)

- [ ] `TravelHeroCard` props에 `placesCount: number` 추가
- [ ] `tripDays` 계산 — `events`가 있을 때 `(마지막 endDate - 첫 startDate + 1)`일, 없을 때 `0`
- [ ] `DashboardInner` 렌더 시 `<TravelHeroCard space={selectedSpace} placesCount={places.length} />` 로 변경

### 3단계 — 검증

- [ ] TypeScript 타입 오류 없음 확인

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` | 수정 | BookingStatus 삭제, TravelHeroCard props 추가 및 통계 실 데이터화 |

---

## 사이드 이펙트 검토

- `BookingStatus`는 외부 import 없음 — 삭제해도 다른 파일 영향 없음
- `TravelHeroCard`는 이 파일 내에서만 사용 — props 변경 영향 없음
- 레이아웃: `MemberStatus + BookingStatus` 2열 → `MemberStatus` 단독으로 바뀌어 가로 폭이 늘어남

---

## 확인 필요 사항

- 없음

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
