---
title: mobile member management
date: 2026-09-23
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
| **작성일** | 2026-09-23 |
| **요구사항 참조** | [[Jeakyoung_Blog/01_Projects/05_ReelTrip/04_VibeCode/02_WorkOrders/2026-09-23-mobile-member-management]] |
| **대상 앱** | Mobile |
| **대상 페이지/화면** | 여행지(`TravelScreen`), 신규 멤버 관리 모달 |
| **작업 유형** | 기능추가 |
| **예상 영향 범위** | `src/features/travel/components/MemberModal.tsx`(신규), `src/features/travel/TravelScreen.tsx` |

---

## 요구사항 분석 요약

- 웹 `MemberScreen`과 동등한 멤버 전체 목록 + 소유자의 멤버 내보내기 기능을 모바일에 추가한다.
- 백엔드 API(`inviteMember`, `removeMember`, 팀스페이스 조회 시 포함되는 `members`)는 이미 존재하며 `removeMember`는 모바일 코드에 정의만 되어 있고 미사용 상태 — 이번에 처음 연결한다.
- [?] **진입 지점**: `TravelScreen` 헤더의 채팅/초대 아이콘 옆에 "멤버" 아이콘 버튼을 추가하는 방식으로 진행 — `InviteModal`과 동일한 패턴이라 UI 일관성에 맞다고 판단해 이대로 진행 (문제 있으면 컨펌 시 변경 요청).
- [?] **삭제 확인 다이얼로그**: 웹은 확인 없이 즉시 삭제하지만, 모바일은 되돌리기 어려운 액션이므로 `Alert.alert`로 확인 후 삭제하도록 추가 — 웹과 동작이 달라지는 부분이라 컨펌 필요.

---

## 작업 계획

### 1단계: 분석 및 준비
- [x] `TeamSpaceResponse`/`MemberResponse` 타입, `inviteMember`/`removeMember` API 시그니처 재확인 (`src/domains/teamspace/api.ts`)
- [x] `useSpaces`/`useInvalidateSpaces` 훅으로 멤버 삭제 후 목록 갱신 가능한지 확인 — `useTravelData`의 `currentSpace`가 `useSpaces()` 결과이므로 `invalidateSpaces()` 호출 시 자동 갱신됨

### 2단계: 구현
- [x] `src/features/travel/components/MemberModal.tsx` 생성: `InviteModal`과 동일한 `Modal`/`formSheet` 패턴, 멤버 목록(아바타 이니셜 + 이름 + 역할 배지), 소유자에게만 다른 멤버 옆 "내보내기" 버튼 노출
- [x] 내보내기 버튼 클릭 시 `Alert.alert`로 확인 → 확인 시 `removeMember` 호출 → 성공 시 `toast.success` + `useInvalidateSpaces()`로 목록 갱신, 실패 시 `toast.error`
- [x] `src/features/travel/TravelScreen.tsx` 헤더에 "멤버" 아이콘 버튼 추가 (채팅/초대 버튼과 같은 줄, `people-outline` 아이콘) → `MemberModal` 오픈

### 3단계: 검증
- [x] `tsc --noEmit` 통과 확인 — 신규 코드로 인한 오류 없음(기존 무관 오류 3건만 존재, `2026-09-21-mobile-backend-full-integration` 완료보고서에서 이미 확인된 것과 동일)
- [ ] 멤버 목록이 실제 팀스페이스 멤버와 일치하는지 확인 — 실기기/시뮬레이터 미실행으로 미검증
- [ ] 소유자 계정에서만 "내보내기" 버튼이 보이는지, 멤버 계정에서는 안 보이는지 확인 — 실기기/시뮬레이터 미실행으로 미검증
- [ ] 멤버 내보내기 후 목록이 갱신되는지, `SpaceInfo`의 아바타 미리보기도 갱신되는지 확인 — 실기기/시뮬레이터 미실행으로 미검증

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `src/features/travel/components/MemberModal.tsx` | 생성 | 멤버 전체 목록 + 소유자용 내보내기 기능 모달 |
| `src/features/travel/TravelScreen.tsx` | 수정 | 헤더에 멤버 관리 진입 아이콘 버튼 추가 |

---

## 사이드 이펙트 검토

- `TravelScreen` 헤더 액션 영역에 아이콘이 하나 더 늘어나(채팅/초대/멤버 3개) 좁은 화면에서 레이아웃 확인 필요.
- 멤버 삭제는 `useInvalidateSpaces()`로 `spaces` 쿼리를 무효화하므로, 홈 화면 팀스페이스 카드 등 `useSpaces`를 쓰는 다른 화면에도 최신 멤버 수가 반영됨 — 의도된 동작이나 참고.

---

## 확인 필요 사항

- [ ] 진입 지점(TravelScreen 헤더 아이콘 버튼)에 동의하는지
- [ ] 삭제 시 `Alert.alert` 확인 다이얼로그 추가(웹과 다르게 동작)에 동의하는지

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
