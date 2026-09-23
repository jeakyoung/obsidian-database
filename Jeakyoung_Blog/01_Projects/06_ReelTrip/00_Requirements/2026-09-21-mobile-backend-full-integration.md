---
title: mobile backend full integration
date: 2026-09-21
type: 요구사항서
project: ReelTrip
status: 컨펌대기
assignee:
  - 안재경
tags: []
---

## 요구사항 정보

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-09-21 |
| **대상 앱** | Mobile |
| **대상 페이지/화면** | 팀스페이스 상세(채팅), 여행/캘린더(할일), 장소 상세(비슷한 장소) |
| **작업 유형** | 기능추가 |
| **우선순위** | 보통 |

---

## 현재 상태 (As-Is)

- 백엔드(`apps/api-spring`)에는 컨트롤러 12개(Auth, Chat/Message, Document, Event, Notification, Place, Recommend, TeamSpace, Todo, UrlParser, User, Root)가 존재.
- 모바일(`apps/mobile`)은 Auth, Event, Notification, Place, TeamSpace, User, UrlParser, Recommend에는 연동되어 있으나:
  - **Chat(`/api/messages`)**: 모바일에 도메인/화면이 전혀 없음. 웹에는 `ChatScreen`(5초 폴링) 구현 완료.
  - **Todo(`/api/todos`)**: 모바일에 도메인/화면이 전혀 없음. 웹에는 CRUD 도메인 완비.
  - **Document(`/api/documents`)**: 벡터 문서 CRUD/유사도 검색 API. 웹에도 대응 화면 없음 — recommend 파이프라인 내부용으로 추정.
  - **"비슷한 장소"/공개 동의(consent)**: `PlaceDetailScreen.tsx`에 `PlaceSimilarSection` UI는 이미 있으나 `similar={[]}` 하드코딩, `onConsent`는 TODO로 비어있음. **대응하는 백엔드 API 자체가 없음** (grep 결과 0건).
  - `PlaceCorrectSection.tsx`: 정정 요청 실패 시 에러 토스트 미표시(`/* TODO: show error toast */`만 존재).

---

## 원하는 상태 (To-Be)

- 모바일이 이미 존재하는 백엔드 기능을 웹과 동일한 수준으로 사용할 수 있도록 연동한다.

---

## 상세 요구사항

### 기능 요구사항
1. **Chat 연동**: `src/domains/chat/api.ts` 신규 생성(`listMessages`, `sendMessage`), 팀스페이스 상세 화면에 채팅 UI/화면 추가, 웹과 동일하게 폴링 방식 적용.
2. **Todo 연동**: `src/domains/todo/api.ts` 신규 생성(`listTodos`, `createTodo`, `updateTodo`, `deleteTodo`), 여행 또는 캘린더 화면에 체크리스트 UI 섹션 추가.
3. [?] **Document(`/api/documents`)**: 사용자 화면 노출이 필요한 기능인지, 아니면 내부 인프라라 모바일 연동 대상에서 제외할지 확인 필요.
4. [?] **"비슷한 장소"/공개 동의**: 대응 백엔드 API가 존재하지 않음. 이번 작업 범위에 **백엔드 신규 개발까지 포함**할지, 아니면 이번엔 제외하고 프론트 UI만 남겨둘지 확인 필요.
5. [?] **에러 토스트 처리(`PlaceCorrectSection.tsx`)**: 기존 `Toast` 유틸 재사용해서 실패 시 에러 표시 추가하는 것도 이번 범위에 포함할지 확인 필요.

### UI/UX 요구사항
- 기존 모바일 디자인 토큰(`src/lib/colors.ts`, `src/lib/styles.ts`) 및 공통 컴포넌트(`Button`, `EmptyState`, `Toast` 등) 재사용.
- 웹의 화면 흐름/동작 방식을 참고하되, 모바일 UX 관례(스크롤, 모달 등)에 맞게 구성.

### 제약 조건
- 백엔드(`apps/api-spring`)는 이미 구현된 Chat/Todo API를 그대로 사용 — 신규 백엔드 개발은 항목 4([?]) 확인 후 결정.
- 요청 범위를 벗어나는 리팩토링(예: `RecommendScreen`의 inline API 호출을 `domains/recommend/api.ts`로 통일하는 것)은 이번 작업에서 제외.

---

## 참고 자료

- 이전 대화에서 도출된 갭 분석 (Chat/Todo 미연동, Document 확인 필요, 비슷한 장소 UI-only 상태)
- 웹 참고 구현: `apps/web/src/domains/chat/api.ts`, `apps/web/src/domains/todo/api.ts`, `apps/web/src/domains/dashboard/components/ChatScreen.tsx`
- 완료보고서 참고: `docs/results/mobile/2026-06-30-chat-service.md` (웹 채팅 구현 시 남긴 잔여 이슈: WebSocket 전환, 페이지네이션, 읽음 처리 — 모바일에도 동일하게 적용될 수 있음)
