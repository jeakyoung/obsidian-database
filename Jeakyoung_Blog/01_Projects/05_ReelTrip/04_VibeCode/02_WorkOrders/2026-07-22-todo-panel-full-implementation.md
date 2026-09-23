---
title: 할 일 패널 전체 구현
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
| **요구사항 참조** | 실DB 전환 작업 #4 — Todo 기능 풀스택 신규 구현 |
| **대상 앱** | Web + API (Spring) |
| **대상 페이지/화면** | `/dashboard` (DashboardScreen > TodoPanel) |
| **작업 유형** | 신규 기능 구현 + 실DB 전환 |
| **예상 영향 범위** | 아래 변경 대상 파일 참고 |

---

## 요구사항 분석 요약

- `DUMMY_TODOS` 구조: `{ label, priority("높음"|"중간"|"낮음"), dday(마감까지 일수) }`
- 기존 이벤트/플레이스와 동일한 패턴(Flyway + MyBatis XML + Service + Controller)으로 구현
- 팀스페이스 단위 할 일 관리 (`space_id` 외래키)
- 우선순위(high/medium/low)와 마감일(due_date) 필드 포함
- 완료 여부(is_done) 포함 — 향후 체크 기능 확장 여지

---

## 작업 계획

### [백엔드]

#### 1단계: DB 마이그레이션
- [ ] `V8__add_todos.sql` 생성
  ```sql
  CREATE TABLE IF NOT EXISTS todos (
      id          BIGSERIAL    PRIMARY KEY,
      space_id    BIGINT       NOT NULL REFERENCES team_spaces(id) ON DELETE CASCADE,
      title       VARCHAR(255) NOT NULL,
      priority    VARCHAR(10)  NOT NULL DEFAULT 'medium',
      due_date    DATE,
      is_done     BOOLEAN      NOT NULL DEFAULT false,
      created_by  BIGINT       NOT NULL REFERENCES users(id),
      created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
      updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()
  );
  ```

#### 2단계: 모델 / DTO
- [ ] `com.reeltrip.api.todo.model.Todo` — Lombok `@Builder` 포함
- [ ] `com.reeltrip.api.todo.dto.CreateTodoRequest` — `spaceId`, `title`, `priority`, `dueDate`
- [ ] `com.reeltrip.api.todo.dto.UpdateTodoRequest` — `title`, `priority`, `dueDate`, `isDone`
- [ ] `com.reeltrip.api.todo.dto.TodoResponse` — 전체 필드 + Lombok `@Builder`

#### 3단계: MyBatis Mapper
- [ ] `com.reeltrip.api.todo.mapper.TodoMapper` (인터페이스)
  - `insert(Todo todo)`
  - `Optional<Todo> findById(Long id)`
  - `List<Todo> findBySpaceId(Long spaceId)`
  - `void update(Todo todo)`
  - `int delete(Long id)`
- [ ] `resources/mapper/TodoMapper.xml` — 위 메서드에 대응하는 SQL

#### 4단계: Service
- [ ] `com.reeltrip.api.todo.service.TodoService` (인터페이스)
- [ ] `com.reeltrip.api.todo.service.TodoServiceImpl`
  - 스페이스 멤버 여부 검증 (`teamSpaceMapper.existsMember`)
  - Event/Place 패턴과 동일하게 구현

#### 5단계: Controller
- [ ] `com.reeltrip.api.todo.controller.TodoController`
  - `POST /api/todos` — 생성
  - `GET /api/todos?spaceId=` — 스페이스 할 일 목록
  - `PUT /api/todos/{id}` — 수정 (완료 체크 포함)
  - `DELETE /api/todos/{id}` — 삭제

#### 6단계: ErrorCode + SecurityConfig 수정
- [ ] `ErrorCode`에 추가:
  - `TODO_NOT_FOUND`
  - `TODO_ACCESS_DENIED`
- [ ] `SecurityConfig`에 추가:
  - `.requestMatchers("/api/todos/**").authenticated()`

---

### [프론트엔드]

#### 7단계: Web API 클라이언트
- [ ] `apps/web/src/domains/todo/api.ts` 신규 생성
  - `TodoResponse` 인터페이스
  - `listTodos(spaceId, token)` — `GET /api/todos?spaceId=`
  - `createTodo(payload, token)` — `POST /api/todos`
  - `updateTodo(id, payload, token)` — `PUT /api/todos/{id}`
  - `deleteTodo(id, token)` — `DELETE /api/todos/{id}`

#### 8단계: DashboardScreen 연동
- [ ] `todos: TodoResponse[]` state 추가
- [ ] `selectedSpaceId` 변경 useEffect에 `listTodos()` fetch 추가 (events/places 패턴 동일)
- [ ] `<TodoPanel todos={todos} />` props 전달

#### 9단계: TodoPanel 컴포넌트 수정
- [ ] `DUMMY_TODOS` 상수 제거
- [ ] `todos: TodoResponse[]` prop 수신
- [ ] 우선순위 매핑: `"high"` → `"높음"` / `"medium"` → `"중간"` / `"low"` → `"낮음"` (+ color 클래스)
- [ ] D-day: `calcDday(todo.dueDate)` 로 계산 (`dueDate` null이면 미표시)
- [ ] 상단 뱃지 카운트: `todos.length` 로 변경 (하드코딩 `3` 제거)
- [ ] 빈 상태: `"할 일이 없습니다"` 메시지

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `apps/api-spring/.../db/migration/V8__add_todos.sql` | 생성 | todos 테이블 Flyway 마이그레이션 |
| `apps/api-spring/.../todo/model/Todo.java` | 생성 | Todo 도메인 모델 |
| `apps/api-spring/.../todo/dto/CreateTodoRequest.java` | 생성 | 생성 요청 DTO |
| `apps/api-spring/.../todo/dto/UpdateTodoRequest.java` | 생성 | 수정 요청 DTO |
| `apps/api-spring/.../todo/dto/TodoResponse.java` | 생성 | 응답 DTO |
| `apps/api-spring/.../todo/mapper/TodoMapper.java` | 생성 | MyBatis 매퍼 인터페이스 |
| `apps/api-spring/.../mapper/TodoMapper.xml` | 생성 | MyBatis SQL XML |
| `apps/api-spring/.../todo/service/TodoService.java` | 생성 | 서비스 인터페이스 |
| `apps/api-spring/.../todo/service/TodoServiceImpl.java` | 생성 | 서비스 구현체 |
| `apps/api-spring/.../todo/controller/TodoController.java` | 생성 | REST 컨트롤러 |
| `apps/api-spring/.../common/exception/ErrorCode.java` | 수정 | TODO_NOT_FOUND, TODO_ACCESS_DENIED 추가 |
| `apps/api-spring/.../config/SecurityConfig.java` | 수정 | `/api/todos/**` authenticated 추가 |
| `apps/web/src/domains/todo/api.ts` | 생성 | Web API 클라이언트 |
| `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` | 수정 | todos 상태·fetch 추가, DUMMY_TODOS 제거, TodoPanel props 전달 |

---

## 사이드 이펙트 검토

- Flyway V8 추가 시 기존 마이그레이션에 영향 없음
- `SecurityConfig` 수정은 기존 엔드포인트 권한에 영향 없음 — todos 추가만
- `ErrorCode` enum 추가는 기존 에러 처리에 영향 없음
- `TodoPanel`은 `DashboardScreen` 내부 컴포넌트 — 외부 사용처 없음

---

## 확인 필요 사항

- [ ] `due_date` NULL 허용 여부 — 제안: **허용** (마감일 없는 할 일 가능)
- [ ] 이번 작업에서 할 일 **생성/삭제 UI** 포함 여부, 아니면 **조회만**?
  - 제안: **조회(read)만** — 대시보드는 요약 뷰, 생성/삭제는 추후 별도 화면

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
