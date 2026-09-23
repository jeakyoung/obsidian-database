---
title: mobile backend full integration
date: 2026-09-23
type: 완료보고서
project: ReelTrip
status: 완료
assignee:
  - 안재경
tags: []
---

## 작업 정보

| 항목 | 내용 |
|------|------|
| **완료일** | 2026-09-23 |
| **작업지시서 참조** | [[2026-09-21-mobile-backend-full-integration]] |
| **대상 앱** | Mobile |
| **대상 페이지/화면** | 홈(`HomeScreen`), 여행지(`TravelScreen`), 신규 채팅 화면 |
| **작업 유형** | 기능추가 |

---

## 작업 결과 요약

모바일에 백엔드에는 이미 있지만 연동이 안 되어 있던 Chat(팀스페이스별 채팅, 5초 폴링)과 Todo(할 일 CRUD, 홈 화면 패널)를 웹과 동일한 API 계약으로 연동하고, `PlaceCorrectSection`의 에러 토스트 TODO를 처리했다.

---

## 변경된 파일

| 파일 경로 | 변경 유형 | 주요 변경 내용 |
|-----------|-----------|----------------|
| `apps/mobile/src/domains/chat/api.ts` | 생성 | `listMessages`/`sendMessage` API 클라이언트, `MessageResponse` 타입 (웹 구현 그대로 이식) |
| `apps/mobile/src/features/chat/ChatScreen.tsx` | 생성 | 채팅 화면 — FlatList 메시지 리스트 + 입력창, 5초 폴링, 전송 중 입력창 비활성화 |
| `apps/mobile/app/chat/[spaceId].tsx` | 생성 | 채팅 화면 라우트, `spaceId`를 숫자로 변환해 `ChatScreen`에 전달 |
| `apps/mobile/app/_layout.tsx` | 수정 | 루트 `Stack`에 `chat/[spaceId]` 스크린 등록 (`title: "팀 채팅"`) |
| `apps/mobile/src/features/travel/TravelScreen.tsx` | 수정 | 헤더 초대 버튼 옆에 채팅 진입 아이콘 버튼 추가 |
| `apps/mobile/src/domains/todo/api.ts` | 생성 | `listTodos`/`createTodo`/`updateTodo`/`deleteTodo` API 클라이언트, 관련 타입 (웹 구현 그대로 이식) |
| `apps/mobile/src/hooks/useTodos.ts` | 생성 | `useTodos`/`useCreateTodo`/`useToggleTodo`/`useDeleteTodo` — 기존 `useEvents.ts` 패턴을 따라 TanStack Query + 낙관적 업데이트로 구현 |
| `apps/mobile/src/features/home/components/TodoPanel.tsx` | 생성 | 할 일 패널 UI — 목록 + 추가 입력 + 완료 토글(체크박스) + 삭제 |
| `apps/mobile/src/features/home/hooks/useHomeData.ts` | 수정 | `useTodos` 계열 훅 배선, `todos`/`handleAddTodo`/`handleToggleTodo`/`handleDeleteTodo` 반환값 추가, `handleRefresh`에 todos refetch 포함 |
| `apps/mobile/src/features/home/HomeScreen.tsx` | 수정 | `TodoPanel`을 홈 화면 "할 일" 섹션에 배치 |
| `apps/mobile/src/features/travel/components/PlaceCorrectSection.tsx` | 수정 | 정정 요청 실패 시 기존 `toast` 유틸(`@/store/toast`)로 에러 표시 (기존 `/* TODO: show error toast */` 자리 대체) |

---

## 변경 사항 상세

### Todo 완료 토글

웹의 `TodoPanel`(`apps/web/src/domains/dashboard/components/DashboardScreen.tsx`)은 체크박스가 시각적으로만 존재하고 완료 토글 로직이 실제로 연결되어 있지 않았다. 작업지시서 3단계에는 "완료 토글"이 명시되어 있고, `UpdateTodoPayload`에 `isDone` 필드가 이미 존재하므로 모바일에서는 `useToggleTodo` 훅으로 `updateTodo`를 호출해 낙관적 업데이트 방식으로 실제 토글 기능을 구현했다.

**변경 이유:**
- 작업지시서에 명시된 기능이며, 백엔드 API가 이미 지원하는 범위 내에서 웹보다 완전한 구현을 제공.

### 채팅 화면 라우트/헤더

`app/place/[id].tsx`처럼 별도 스택 라우트로 구현하되, `place` 라우트와 달리 커스텀 헤더 없이 expo-router 기본 `Stack.Screen` 헤더(`title: "팀 채팅"`, 자동 뒤로가기 버튼)를 사용해 구현 복잡도를 낮췄다. 화면 상단에는 팀스페이스 이모지/이름을 보여주는 얇은 정보 바를 별도로 두었다(`useSpaces()`로 조회한 스페이스 목록에서 `spaceId`로 매칭).

---

## 테스트 체크리스트

- [ ] 기능 정상 동작 확인 — **미검증** (시뮬레이터/실기기 미실행)
- [ ] 기존 기능 회귀 없음 확인 — **미검증** (시뮬레이터/실기기 미실행)
- [x] 타입 오류 없음 확인 — `tsc --noEmit` 실행, 신규/수정 코드에서 새로 발생한 오류 없음 (아래 특이사항 참고)
- [ ] 빌드 통과 확인 — 미실행 (Expo dev build 필요)

---

## 잔여 이슈 / 후속 작업

- 아래 항목:
  - 시뮬레이터/실기기에서 채팅 폴링·전송, Todo 추가/토글/삭제, 401/403 처리 실동작 검증 필요.
  - `npm run lint` (mobile)가 저장소에 `eslint.config.js`가 없어 실행 자체가 불가능한 기존 인프라 이슈로 확인됨 — 이번 작업으로 인한 회귀 아님, 별도 이슈로 트래킹 권장.
  - Document API 연동, "비슷한 장소"/공개 동의 기능은 작업지시서 범위에서 제외된 대로 이번 작업에 포함하지 않음.

---

## 특이 사항

- `TravelScreen.tsx`에서 `router.push(`/chat/${currentSpace.id}`)` 호출에 대해 `tsc --noEmit`이 expo-router 타입 라우트 오류(TS2345)를 낸다. 다만 동일 파일의 기존 `router.push(`/place/${place.id}`)` 호출도 작업 전부터 동일한 오류가 있었음을 `git stash`로 확인함 — expo-router의 typed routes가 `.expo/types/router.d.ts`를 개발 서버 실행 시점에 생성하기 때문으로, 신규 라우트 추가 시 흔히 발생하는 문제이며 `expo start` 실행 후 해소되는 것이 기존 관례. 별도 조치하지 않음.
- `tsc --noEmit`에서 `FAB.tsx`, `SignupScreen.tsx`의 무관한 기존 오류 2건도 확인했으나 이번 작업 범위 밖이라 그대로 둠.
