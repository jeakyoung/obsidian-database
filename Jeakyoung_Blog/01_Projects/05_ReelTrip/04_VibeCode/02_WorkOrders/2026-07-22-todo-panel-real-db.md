---
title: 할 일 패널 실 DB 연동
date: 2026-07-22
type: 작업지시서
project: ReelTrip
status: 완료 (todo-panel-full-implementation으로 대체됨)
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
| **요구사항 참조** | 실DB 전환 작업 #4 — TodoPanel (DUMMY_TODOS) |
| **대상 앱** | Web |
| **대상 페이지/화면** | `/dashboard` (DashboardScreen > TodoPanel) |
| **작업 유형** | 실DB 전환 |
| **예상 영향 범위** | dashboard/DashboardScreen.tsx |

---

## 요구사항 분석 요약

`DUMMY_TODOS`를 실DB로 전환하려 했으나 **백엔드에 todos API가 존재하지 않습니다.**

- Spring API 전체 패키지 확인 결과: `todo` 패키지 없음
- DB 마이그레이션(V1~V7) 확인 결과: `todos` 테이블 없음
- Web `domains/` 확인 결과: `todo` 도메인 없음

따라서 1~3번과 달리 이번은 "연동" 작업이 아닌 **방향 결정**이 먼저 필요합니다.

**현재 DUMMY_TODOS 구조:**
```ts
{ label: "숙소 예약하기",     priority: "높음", dday: 2 }
{ label: "렌터카 확정하기",   priority: "중간", dday: 5 }
{ label: "일정 투표 참여하기", priority: "낮음", dday: 7 }
```

---

## 선택지

### A안 — pending 이벤트로 대체 (추천)
이미 fetch된 `selectedSpace.events` 중 `status: "pending"` 인 이벤트를 할 일 목록으로 표시합니다.

- 추가 API 호출 없음 (이미 events 로드됨)
- `EventResponse.status === "pending"` 항목을 `TodoPanel`에 전달
- 표시 내용: 이벤트 제목 + 시작일까지 D-day 계산
- priority 개념 없으므로 해당 UI 제거, D-day만 표시
- pending 이벤트 없으면 "확인이 필요한 일정이 없습니다" 빈 상태

**단점:** 기획 의도(숙소·항공 예약 체크리스트)와 다소 다를 수 있음

---

### B안 — 패널 숨김 (가장 단순)
TodoPanel을 임시 제거하고, todos API 구현 이후 복원합니다.

- 코드 변경 최소화
- 우측 패널에 `ActivityPanel` 단독으로 올라오게 됨
- DUMMY 코드만 남아있는 상태 해소

---

### C안 — todos API 신규 구현 (범위 초과)
백엔드에 `todos` 테이블·API를 신규 구현합니다.

- Spring: 마이그레이션 + mapper + service + controller
- Web: `domains/todo/` 도메인 신규 생성
- 실DB 전환 작업 범위를 벗어나는 신규 기능 개발

---

## 확인 필요 사항

- [ ] **A안 / B안 / C안 중 어느 방향으로 진행할지 결정 필요**
  - 제안: **A안** — 추가 공수 없이 실 데이터를 활용할 수 있고, 추후 todos API 구현 시 교체 용이

---

## 컨펌

- [ ] A안으로 진행 승인
- [ ] B안으로 진행 승인
- [ ] C안으로 진행 승인 (별도 일정 조율 필요)
- [ ] 수정 후 재검토 필요
