---
title: mobile backend full integration
date: 2026-09-21
type: 작업지시서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

## 작업 개요

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-09-21 |
| **요구사항 참조** | docs/orders/2026-09-21-mobile-backend-full-integration.md |
| **대상 앱** | Mobile |
| **대상 페이지/화면** | 홈(`HomeScreen`), 여행지(`TravelScreen`), 신규 채팅 화면 |
| **작업 유형** | 기능추가 |
| **예상 영향 범위** | `src/domains/chat/*`(신규), `src/domains/todo/*`(신규), `src/features/travel/*`, `src/features/home/*`, `app/` 라우트 1개 신규 |

---

## 요구사항 분석 요약

- 백엔드에 이미 존재하지만 모바일에 연동이 안 된 두 기능(Chat, Todo)을 웹과 동일한 API 계약으로 연동한다.
- Chat: 팀스페이스별 메시지 목록 조회(GET `/api/messages?spaceId=`) + 전송(POST `/api/messages`), 5초 폴링 — 웹 `ChatScreen.tsx` 방식을 그대로 이식.
- Todo: 팀스페이스별 할일 CRUD(GET/POST/PUT/DELETE `/api/todos`) — 웹은 `DashboardScreen`의 우측 `TodoPanel`(추가/삭제)로 구현되어 있음. 모바일은 이와 동등한 패널을 **홈 화면**에 배치 (모바일 홈이 웹 대시보드에 대응).
- Chat 화면은 웹처럼 별도 페이지 형태 — 모바일은 별도 탭 대신 **여행지(`TravelScreen`) 헤더의 아이콘 버튼**을 눌러 진입하는 신규 라우트(`app/chat/[spaceId].tsx`)로 구현 (하단 탭 5개로 늘리는 것보다 기존 초대 버튼과 동일한 패턴이 UI 일관성에 맞음).
- [?] **Document(`/api/documents`)**: 이번 작업 범위에서 **제외**. 사용자 화면 노출이 필요하면 별도 요구사항으로 진행 요청.
- [?] **"비슷한 장소"/공개 동의**: 대응 백엔드 API가 없어 "연동"이 불가능 — 이번 작업 범위에서 **제외**. 신규 개발이 필요하면 별도 요구사항서로 백엔드 설계부터 진행 요청.
- [?] **`PlaceCorrectSection.tsx` 에러 토스트**: 기존 `Toast` 유틸 재사용해 함께 처리 — 간단한 수정이라 이번 작업에 **포함**하는 것으로 진행 (문제 있으면 컨펌 시 제외 요청).

---

## 작업 계획

### 1단계: 분석 및 준비
- [x] 백엔드 Chat/Todo 컨트롤러·DTO 확인 (`MessageController`, `TodoController`)
- [x] 웹 참고 구현 확인 (`apps/web/src/domains/chat/api.ts`, `apps/web/src/domains/dashboard/components/DashboardScreen.tsx`의 `TodoPanel`)
- [x] 모바일 `api-client.ts` 요청 패턴 재확인(토큰 갱신 흐름과 충돌 없는지) — `apiRequest`가 401 시 자체 refresh/재시도하므로 그대로 사용, 별도 처리 불필요

### 2단계: 구현 — Chat
- [x] `src/domains/chat/api.ts` 생성: `listMessages(spaceId, token)`, `sendMessage(spaceId, content, token)`, `MessageResponse` 타입
- [x] `src/features/chat/ChatScreen.tsx` 생성: 메시지 리스트(FlatList) + 입력창, 5초 폴링(`useEffect` + `setInterval`, 언마운트 시 정리), 전송 중 입력창/버튼 disable
- [x] `app/chat/[spaceId].tsx` 라우트 생성 → `ChatScreen`에 `spaceId` 전달 (`app/_layout.tsx`의 루트 `Stack`에도 등록)
- [x] `src/features/travel/TravelScreen.tsx` 헤더에 채팅 진입 아이콘 버튼 추가 (초대 버튼 옆)

### 3단계: 구현 — Todo
- [x] `src/domains/todo/api.ts` 생성: `listTodos`, `createTodo`, `updateTodo`, `deleteTodo`, `TodoResponse`/`CreateTodoPayload`/`UpdateTodoPayload` 타입
- [x] `src/features/home/components/TodoPanel.tsx` 생성: 할일 목록 + 추가 입력 + 완료 토글 + 삭제
- [x] `src/hooks/useTodos.ts` 생성 (기존 `useEvents.ts` 패턴을 따라 TanStack Query + 낙관적 업데이트로 구현) + `src/features/home/hooks/useHomeData.ts`에 todos 상태/핸들러 배선 (스페이스 선택 시 `listTodos` 호출)
- [x] `src/features/home/HomeScreen.tsx`에 `TodoPanel` 배치

### 4단계: 부가 수정
- [x] `src/features/travel/components/PlaceCorrectSection.tsx`: 정정 요청 실패 시 `Toast` 유틸로 에러 표시

### 5단계: 검증
- [x] `tsc --noEmit` 통과 확인 (기존에 있던 무관한 에러 3건 제외 — 상세는 완료보고서 참고)
- [ ] `lint` — 저장소의 `eslint.config.js` 부재로 실행 불가 (기존 인프라 이슈, 이번 작업 범위 밖)
- [ ] 채팅 목록 조회/전송/폴링 동작 확인, 화면 이탈 시 polling 정리 확인 — 실기기/시뮬레이터 미실행으로 미검증
- [ ] 할일 추가/완료토글/삭제 동작 확인, 스페이스 전환 시 목록 갱신 확인 — 실기기/시뮬레이터 미실행으로 미검증
- [ ] 비멤버/토큰 만료 상태에서의 401/403 처리 확인 — 실기기/시뮬레이터 미실행으로 미검증

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `src/domains/chat/api.ts` | 생성 | listMessages/sendMessage API 클라이언트 |
| `src/features/chat/ChatScreen.tsx` | 생성 | 채팅 화면 (리스트+입력창+폴링) |
| `app/chat/[spaceId].tsx` | 생성 | 채팅 화면 라우트 |
| `src/features/travel/TravelScreen.tsx` | 수정 | 채팅 진입 버튼 추가 |
| `src/domains/todo/api.ts` | 생성 | Todo CRUD API 클라이언트 |
| `src/features/home/components/TodoPanel.tsx` | 생성 | 할일 패널 UI |
| `src/features/home/hooks/useHomeData.ts` | 수정 | todos 상태/핸들러 추가 |
| `src/features/home/HomeScreen.tsx` | 수정 | TodoPanel 배치 |
| `src/features/travel/components/PlaceCorrectSection.tsx` | 수정 | 실패 시 에러 토스트 표시 |

---

## 사이드 이펙트 검토

- `HomeScreen`에 패널이 추가되어 레이아웃(스크롤 높이 등)이 변경될 수 있음 — 기존 이벤트/스페이스 카드 영역과 겹치지 않는지 확인 필요.
- `TravelScreen` 헤더에 버튼이 하나 추가되어(초대 버튼 옆) 좁은 화면에서 레이아웃 확인 필요.
- 신규 폴링(채팅 5초)이 기존 TanStack Query 캐싱과 별도로 동작 — 배터리/네트워크 사용량 증가는 웹과 동일한 수준(잔여 이슈로 기존에도 인지됨, `docs/results/mobile/2026-06-30-chat-service.md`).
- Document API, 비슷한 장소/동의 기능은 이번 변경에 포함되지 않음 — 관련 화면(`PlaceSimilarSection`)은 현재 상태(빈 배열) 그대로 유지.

---

## 확인 필요 사항

- [ ] Document API 연동 제외에 동의하는지
- [ ] "비슷한 장소"/공개 동의 기능은 백엔드 미비로 이번 범위 제외에 동의하는지
- [ ] Chat 진입 방식(하단 탭 추가가 아니라 여행지 화면 아이콘 버튼)에 동의하는지
- [ ] Todo 패널 위치(홈 화면)에 동의하는지
- [ ] `PlaceCorrectSection` 에러 토스트 수정을 이번 범위에 포함해도 되는지

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
