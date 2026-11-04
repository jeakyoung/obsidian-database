---
title: 모바일 멤버 관리
date: 2026-09-23
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
| **작성일** | 2026-09-23 |
| **대상 앱** | Mobile |
| **대상 페이지/화면** | 여행지(`TravelScreen`), 신규 멤버 관리 화면/모달 |
| **작업 유형** | 기능추가 |
| **우선순위** | 보통 |

---

## 현재 상태 (As-Is)

- 백엔드에는 멤버 조회(팀스페이스 응답에 포함된 `members`)/초대(`POST /api/teamspaces/{id}/members`)/삭제(`DELETE /api/teamspaces/{id}/members/{userId}`) API가 모두 존재.
- 웹에는 `MemberScreen`(`apps/web/src/domains/dashboard/components/MemberScreen.tsx`)이 있어 전체 멤버 목록 조회, 소유자만 보이는 "내보내기"(삭제) 버튼, 역할 안내를 제공.
- 모바일은 `InviteModal`(`apps/mobile/src/features/travel/components/InviteModal.tsx`)로 초대만 가능하고, `SpaceInfo.tsx`에 멤버 아바타 4명까지만 미리보기로 노출될 뿐 전체 목록 조회·삭제 화면이 없음.
- 모바일 `src/domains/teamspace/api.ts`에는 이미 `removeMember` 함수가 정의되어 있으나 어디에서도 호출되지 않음(사용처 없음, 데드 코드 상태).

---

## 원하는 상태 (To-Be)

- 모바일에서도 웹과 동등한 수준으로 팀스페이스 멤버 전체 목록을 확인하고, 소유자는 멤버를 내보낼 수 있다.

---

## 상세 요구사항

### 기능 요구사항
1. 팀스페이스 전체 멤버 목록을 볼 수 있는 화면/모달을 신규로 추가한다.
2. 소유자(`role === "owner"`)로 로그인한 경우에만, 본인을 제외한 멤버 옆에 "내보내기" 액션을 노출하고 `removeMember` API를 호출한다.
3. 목록에는 아바타(이니셜), 이름, 역할 배지(소유자/멤버)를 표시한다 (웹 `MemberScreen`과 동일한 정보).
4. [?] **진입 지점**: `TravelScreen` 헤더에 채팅/초대 버튼과 나란히 "멤버" 아이콘 버튼을 추가하는 방식으로 진행할지, 아니면 `SpaceInfo`의 아바타 영역을 탭하면 열리는 방식으로 진행할지 확인 필요.
5. [?] **삭제 확인**: 웹은 별도 확인 없이 바로 "내보내기" 버튼 클릭으로 삭제되는데, 모바일은 되돌리기 어려운 액션이니 확인 다이얼로그(RN `Alert.alert`)를 추가할지, 아니면 웹과 동일하게 즉시 삭제로 맞출지 확인 필요.

### UI/UX 요구사항
- 기존 `InviteModal`과 동일한 패턴(RN `Modal`, `presentationStyle="formSheet"`, `modalHeader` 스타일)으로 구현해 일관성 유지.
- 디자인 토큰(`src/lib/colors.ts`, `src/lib/styles.ts`) 재사용.

### 제약 조건
- 요청 범위를 벗어나는 역할 변경(소유권 이전 등)은 포함하지 않는다 — 웹에도 없는 기능.
- 백엔드 API 변경 없이 기존 엔드포인트만 사용한다.

---

## 참고 자료

- 웹 참고 구현: `apps/web/src/domains/dashboard/components/MemberScreen.tsx`
- 모바일 기존 패턴: `apps/mobile/src/features/travel/components/InviteModal.tsx`, `apps/mobile/src/hooks/useSpaces.ts`
