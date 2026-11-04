---
title: 대시보드 더미 정리 (BookingStatus 제거)
date: 2026-08-20
type: 작업
project: ReelTrip
status: 완료
priority: 보통
assignee:
  - 안재경
tags: []
---

# 대시보드 더미 정리 (BookingStatus 제거)

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-08-20 |
| **대상 시스템** | Web |
| **관련 화면·프로그램** | `DashboardScreen.tsx` |

> 7월에 하던 실DB 전환 작업 잔여분 정리. 이번엔 "연동" 대신 "제거"를 택한 케이스

## 🔍 현상 및 원인

`BookingStatus` 컴포넌트가 항공권/숙소/렌터카/액티비티 예약 현황을 여전히 하드코딩으로 보여주고 있었다. 예약 관리 자체가 이 서비스 범위 밖(예약 시스템을 만들 계획이 없음)이라 실 데이터로 바꿀 대상이 아니라고 판단, 아예 제거하는 쪽으로 정리했다.

`TravelHeroCard`의 통계 카드 4개 중 "저장된 장소"(12개 고정), "일정"(4일 고정)도 여전히 하드코딩 상태였다. 이건 [[팀스페이스 이벤트 실 데이터 연동]] / [[저장된 장소 섹션 실 데이터 전환]]에서 이미 `places`, `events`를 fetch하고 있었으니 그 값을 그대로 갖다 쓰면 되는 거라 별도 API 호출 없이 바로 해결 가능했다.

## 🔧 조치 내용

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| 삭제 | `BookingStatus` | 컴포넌트 전체 제거, 렌더 호출부 제거 |
| 레이아웃 | `MemberStatus` | 2열(멤버+예약현황) → 단독 전체 폭으로 변경 |
| 화면 | `TravelHeroCard` | `placesCount: number` prop 추가 |

```
저장된 장소: "12개"(하드코딩) → `${placesCount}개` (= places.length)
일정:        "4일"(하드코딩)  → `${tripDays}일` (이벤트 기간 계산, 없으면 "-")
참여 멤버:   기존 실 데이터 그대로 유지
예약 완료:   항목 자체를 제거 (BookingStatus 제거와 일관성)
```

`tripDays`는 `(마지막 이벤트 endDate − 첫 이벤트 startDate + 1)`일로 계산했다.

## ✅ 검증 및 결과

- [x] TypeScript 타입 오류 없음 (`tsc --noEmit`)
- [x] 저장된 장소/이벤트 있는 space에서 실제 개수·일수 표시 확인
- [x] 이벤트 없는 space에서 "-" 표시 확인
- [x] BookingStatus 패널이 화면에서 완전히 사라졌는지 확인

## 🔗 참고

- `docs/orders/2026-08-20-real-db-migration.md`
- `docs/workOrders/2026-08-20-dashboard-dummy-cleanup.md`
- `docs/results/2026-08-20-dashboard-dummy-cleanup.md`

> **남은 것**: `AiScreen.tsx`의 `DUMMY_AI_RECS`, TravelHeroCard의 "65% 준비 진행률" 같은 값들은 이번 범위 밖으로 그대로 둠. [[ReelTrip 프로젝트 개요]] 참고.
