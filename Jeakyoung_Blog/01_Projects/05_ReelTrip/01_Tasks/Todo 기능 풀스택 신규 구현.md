---
title: Todo 기능 풀스택 신규 구현
date: 2026-07-22
type: 작업
project: ReelTrip
status: 완료
priority: 높음
assignee:
  - 안재경
tags: []
---

# Todo 기능 풀스택 신규 구현

## 📋 개요

| 항목 | 내용 |
|:--|:--|
| **요청자** | — |
| **요청일** | 2026-07-22 |
| **대상 시스템** | Web + API (Spring) |
| **관련 화면·프로그램** | `DashboardScreen.tsx` > TodoPanel, `todo` 패키지 (Spring) |

> "더미 걷어내기" 작업인 줄 알고 시작했다가, 걷어낼 API 자체가 없어서 새로 만들게 된 케이스

## 🔍 현상 및 원인

다른 섹션([[팀스페이스 이벤트 실 데이터 연동]], [[스케줄 타임라인 실 데이터 전환]], [[저장된 장소 섹션 실 데이터 전환]])처럼 `TodoPanel`의 `DUMMY_TODOS`도 실 API로 바꾸려고 봤더니, Spring 쪽에 `todo` 패키지 자체가 없고 DB 마이그레이션(V1~V7)에도 `todos` 테이블이 없었다. Web `domains/`에도 todo 도메인이 없음. "연동"이 아니라 "새로 만들지 말지" 결정부터 필요한 상황.

## 🔧 조치 내용

세 가지 방향을 놓고 골랐다.

| 안 | 내용 | 비고 |
|:--|:--|:--|
| A | 이미 fetch된 `pending` 상태 이벤트를 할 일처럼 표시 | 추가 API 불필요, 다만 기획 의도(숙소·항공 체크리스트)랑 다름 |
| B | TodoPanel 패널 자체를 임시 숨김 | 코드 변경 최소, 기능 자체가 사라짐 |
| C | todos 테이블·API를 풀스택으로 신규 구현 | 범위는 크지만 실제로 쓸 수 있는 기능이 됨 |

A안이 공수는 제일 적었지만 "할 일 관리"라는 기능 자체를 흉내만 내는 셈이라 만족스럽지 않아서, C안(풀스택 신규 구현)으로 진행했다.

| 구분 | 대상 | 변경 내용 |
|:--|:--|:--|
| DB | `V8__add_todos.sql` | `todos` 테이블 (space_id, title, priority, due_date, is_done) |
| 백엔드 | `todo` 패키지 | model/dto/mapper/service/controller — Event/Place와 동일한 레이어 패턴 |
| 백엔드 | `ErrorCode` | `TODO_NOT_FOUND`, `TODO_ACCESS_DENIED` 추가 |
| 백엔드 | `SecurityConfig` | `/api/todos/**` 인증 경로 추가 |
| 프론트 | `domains/todo/api.ts` | `listTodos` / `createTodo` / `updateTodo` / `deleteTodo` |
| 프론트 | `TodoPanel` | 생성 입력창(Enter 지원) + 삭제(×) 버튼 포함해서 실 CRUD로 교체 |

정렬은 `TodoMapper.xml`에서 priority(high→medium→low) → due_date 오름차순 → created_at 순으로 처리했다. 우선순위 뱃지는 `high`→빨강, `medium`→주황, `low`→초록.

## ✅ 검증 및 결과

- [x] TypeScript 타입 오류 없음 (`tsc --noEmit`)
- [x] Flyway V8 마이그레이션 자동 적용 확인
- [x] 할 일 추가/삭제가 목록에 즉시 반영되는지 확인
- [x] space 전환 시 해당 space의 todos만 로드되는지 확인

## 🔗 참고

- `docs/workOrders/2026-07-22-todo-panel-real-db.md` (방향 결정 문서)
- `docs/workOrders/2026-07-22-todo-panel-full-implementation.md` (C안 구현 계획)
- `docs/results/2026-07-22-todo-panel-full-implementation.md`

> **남은 것**: 완료 체크(isDone 토글) UI, 우선순위 변경 UI는 미구현 — 생성 시 항상 `medium` 고정. 다음에 붙일 것.
