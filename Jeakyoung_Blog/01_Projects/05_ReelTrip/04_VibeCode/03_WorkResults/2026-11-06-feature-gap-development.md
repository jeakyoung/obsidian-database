---
title: 모노레포 전반 기능 격차 조사 및 추가개발
date: 2026-11-06
type: 완료보고서
project: ReelTrip
status: 완료
assignee: []
tags: []
---

## 작업 정보

| 항목 | 내용 |
|------|------|
| **완료일** | 2026-11-06 |
| **작업지시서 참조** | (요구사항서/작업지시서 생략 — herdr 멀티에이전트 팀 워크플로의 `.team/PLAN.md`, `.team/TASKS.md`로 목표 승인 대체) |
| **대상 앱** | Web / Mobile / API / DB (공통) |
| **대상 페이지/화면** | 프로필, AI 추천, 대시보드 Todo, 팀스페이스 설정, 알림, 알림 설정 |
| **작업 유형** | 기능추가 (기능 격차 조사 기반 추가개발) |

---

## 작업 결과 요약

모노레포(apps/web, apps/mobile, apps/api-spring, DB)를 전수 조사해 "미구현/필요한 기능" 7건(세부 14개 작업 항목)을 식별하고, 사용자 전체 승인을 받아 묶음 A(빠른 승리 5건)·묶음 B(알림 생성 로직 5건)·묶음 C(알림 설정 저장 4건)로 나눠 전부 구현했다.

---

## 변경된 파일

| 파일 경로 | 변경 유형 | 주요 변경 내용 |
|-----------|-----------|----------------|
| `apps/mobile/src/domains/user/api.ts` | 수정 | `getProfile()` 경로 버그 수정(`/api/profile` → `/api/user/profile`), `updateProfile` wrapper 신설 |
| `apps/web/src/domains/recommend/api.ts` | 생성 | 웹 AI 추천 실연동용 `/api/recommend` wrapper |
| `apps/web/src/domains/dashboard/components/AiScreen.tsx` | 수정 | 더미 추천(`DUMMY_AI_RECS`) 제거, 실제 API 연동(로딩/에러/빈 상태 포함) |
| `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` | 수정 | Todo 위젯에 완료토글(`updateTodo`)/우선순위/마감일 UI 추가 |
| `apps/mobile/src/domains/teamspace/api.ts` | 수정 | `updateTeamSpace`/`deleteTeamSpace`/`listMembers` wrapper 추가 |
| `apps/mobile/src/features/travel/components/SpaceSettingsModal.tsx` | 생성 | 팀스페이스 이름/이모지 수정 + 삭제 화면 (오너만 편집) |
| `apps/web/src/domains/dashboard/components/SettingsScreen.tsx` | 수정 | 프로필 폼 실연동, 알림 설정 토글 실연동 |
| `apps/mobile/src/domains/user/api.ts`, `.../EditProfileModal.tsx` | 생성/수정 | 모바일 프로필 수정 폼 |
| `apps/api-spring/.../notification/service/NotificationService.java`, `impl/NotificationServiceImpl.java` | 수정 | 알림 `create()` 메서드 신설, best-effort 예외 처리, 설정값 반영 |
| `apps/api-spring/.../notification/mapper/NotificationMapper.java`, `NotificationMapper.xml` | 수정 | `insert` 매핑 추가 |
| `apps/api-spring/.../teamspace/service/TeamSpaceServiceImpl.java` | 수정 | 초대/제거 시 알림 생성 |
| `apps/api-spring/.../event/service/EventServiceImpl.java` | 수정 | 일정 추가/변경 시 알림 생성 |
| `apps/api-spring/.../place/service/PlaceServiceImpl.java` | 수정 | 장소 확정/추가 시 알림 생성 |
| `apps/api-spring/.../chat/service/MessageServiceImpl.java` | 수정 | 채팅 메시지 알림 생성 |
| `apps/api-spring/src/main/resources/db/migration/V9__add_notification_settings.sql` | 생성 | 알림 설정 테이블 신설 |
| `apps/api-spring/.../notification/controller/NotificationController.java` | 수정 | 설정 조회/저장 엔드포인트(`GET/PUT /api/notifications/settings`) |
| `apps/mobile/src/features/.../NotificationSettingsModal.tsx` | 생성 | 모바일 알림 설정 화면 신설 |

총 16개 커밋 (da7f827 이전 버그수정 사이클과 별개, `e6f72f7`~`1c8d1b9`).

---

## 변경 사항 상세

### 1. 묶음 A — 빠른 승리 (5건)

- **모바일 getProfile 경로 버그**: `/api/profile` → `/api/user/profile`로 수정. 이전엔 항상 404라 프로필 화면이 빈 값이었음.
- **웹 AI 추천 실연동**: `AiScreen.tsx`가 하드코딩 더미 3건만 보여주던 것을 실제 `/api/recommend` 호출로 교체(모바일은 이미 실연동 상태였음).
- **웹 Todo 위젯 보완**: 완료 토글, 우선순위 선택, 마감일 입력 UI 추가(백엔드 API는 기존 재사용).
- **모바일 팀스페이스 수정/삭제 화면**: 웹에만 있던 기능을 모바일에 포팅. 오너만 편집 가능하도록 UI+서버 양쪽에서 방어.
- **프로필 수정 폼**: 웹에 폼 추가, 모바일에 wrapper+모달 신설.

### 2. 묶음 B — 알림 생성 로직 (5건)

**변경 전:** `notifications` 테이블/서비스/컨트롤러는 있지만 알림을 생성(INSERT)하는 코드가 백엔드 전체에 전무해, 모든 사용자의 알림 목록이 항상 빈 상태였다.

**변경 후:** `NotificationService.create()`를 신설하고, 팀스페이스 초대/제거·일정 추가/변경·장소 확정/추가·채팅 메시지 발생 시 각각 알림을 생성하도록 연결했다. 모든 경로에서 행위자 본인은 제외하고 나머지 멤버에게만 알림이 간다.

**변경 이유 / 리뷰 과정에서 발견·수정된 문제:**
- 1차 리뷰에서 `create()`가 예외를 흡수하지 않아, 알림 INSERT가 실패하면(예: 커넥션 풀 고갈) 이미 성공한 초대/일정/장소/채팅 작업 전체가 HTTP 500으로 보이는 문제가 발견됨 — 저장소 전체에 `@Transactional`이 없어 메인 작업은 이미 커밋된 상태인데 응답만 실패로 보이는 사용자 체감 버그였음. `create()` 내부를 try/catch로 감싸 알림은 best-effort로 동작하도록 수정(커밋 `3f0ff68`).

### 3. 묶음 C — 알림 설정 저장 (4건 + 리뷰 후속 1건)

**변경 전:** 웹 설정 화면의 알림 토글 4개(새 장소/일정변경/멤버참여/AI추천)가 로컬 state만 바꾸고 새로고침하면 항상 기본값으로 리셋되었다. 모바일에는 이 화면 자체가 없었다.

**변경 후:** `V9__add_notification_settings.sql` 마이그레이션으로 설정 테이블을 신설하고, `GET/PUT /api/notifications/settings`(JWT에서 유도한 본인 userId만 사용, 요청 바디로 다른 사용자 설정을 건드릴 수 없음)를 추가. 웹은 실제 API 연동, 모바일은 신규 화면(`NotificationSettingsModal`)을 만들었다.

**변경 이유 / 리뷰 과정에서 발견·수정된 문제:**
- 1차 리뷰에서 "설정을 저장은 되지만 실제 알림 생성 로직(묶음 B)이 이 설정값을 전혀 참조하지 않아, 토글을 꺼도 알림이 계속 온다"는 더 근본적인 문제가 발견됨. `NotificationServiceImpl.create()`에 설정 체크를 추가해(커밋 `1c8d1b9`) `member`/`schedule`/`place` 타입은 대응 토글이 꺼져 있으면 알림 생성을 건너뛰도록 수정했다. `chat`은 설정 화면에 대응 토글이 없어 항상 생성되도록 두었고, `aiRecommend` 토글은 AI 추천이 원래 알림을 만들지 않는 동기 응답 구조라 그대로 두었다(죽은 설정으로 남음, 범위 밖).

---

## 테스트 체크리스트

- [ ] 기능 정상 동작 확인 — **미검증** (실제 앱/서버 실행 환경에서 수동 확인 필요)
- [ ] 기존 기능 회귀 없음 확인 — **미검증**
- [x] 타입 오류 없음 확인 — 리뷰 단계에서 `apps/web`·`apps/mobile` `npx tsc --noEmit`, `apps/api-spring` `mvn -o compile`을 매 묶음마다 직접 실행해 확인(모두 클린, 기존에 있던 무관한 사전 오류만 남음)
- [ ] 빌드 통과 확인 — 미실행

> herdr 멀티에이전트 팀(planner/researcher/worker/reviewer)이 조사 → 사용자 컨펌 → 구현 → 리뷰 → (문제 발견 시) 재작업 → 재검토 순서로 진행했다. 리뷰 단계에서 두 차례(묶음 B, 묶음 C) 실질적인 CHANGES REQUESTED가 나와 재작업으로 이어졌고, 최종적으로 16개 커밋 전부 APPROVED로 종료되었다(`.team/REVIEW.md` 참조). 다만 코드 추적/컴파일 기준 검증이며, 실제 앱 실행·DB 마이그레이션 적용 등 런타임 검증은 하지 않았다.

---

## 잔여 이슈 / 후속 작업

- 아래 항목:
  - **백로그로 보류한 항목(이번 범위 밖)**: `documents`(pgvector) 자동 적재 파이프라인, documents 관리 UI, `users.role` 기반 관리자 기능, 모바일 "비슷한 장소" 추천(백엔드 설계 필요), 장소 공개동의 저장(정책 검토 필요). 전부 별도 요구사항지시서가 필요하다고 안내함.
  - **알림 설정-알림 매핑 설계 공백**: `aiRecommend` 토글은 대응하는 알림이 원천적으로 생성되지 않아 현재 UI상 "죽은 설정"으로 남아 있다. 채팅 알림은 설정 화면에 끄는 방법이 UI에도 없다(항상 켜짐). 토글을 추가/제거할지는 별도 UX 결정이 필요.
  - `notificationMapper`의 신설 `insert`가 멤버 수만큼 반복 호출(N회)되는 구조로, 정확성을 우선해 구현했고 성능 최적화(배치 처리)는 하지 않았다 — 팀스페이스 통상 규모에서는 문제가 되지 않을 것으로 판단.
  - 전체 커밋은 로컬에서만 생성되었고, 아직 원격 push 여부는 사용자 확인 전이다(이전 버그수정 사이클과 동일하게 필요 시 안내 후 push 진행).

---

## 특이 사항

- herdr 멀티에이전트 팀 워크플로(`.team/PLAN.md`, `RESEARCH.md`, `TASKS.md`, `REVIEW.md`, `LOG.md`)로 조사 → 우선순위 확정 → 사용자 컨펌 → 구현 → 리뷰까지 전 과정을 진행했다. 사용자가 "전부 다 개발"을 선택해 묶음 A/B/C(총 14개 계획 항목 + 리뷰 후속 2건, 16개 커밋)를 전부 완료했다.
- 작업 중 세션이 한 번 중단되어(묶음 A [3] 작업 중 JSX 태그가 깨진 채 미완성 상태로 남음) 재개 시 git diff로 정확한 중단 지점을 파악하고 고쳐서 이어간 사례가 있었다.
- 리뷰어가 두 차례(묶음 B의 예외 전파, 묶음 C의 설정-알림 미연동) 실질적인 버그를 발견해 재작업으로 이어졌다 — 두 문제 모두 "개별 커밋은 지시대로 정확히 구현됐지만 묶음 전체의 의도(알림은 best-effort여야 한다, 설정은 알림 생성에 실제 영향을 줘야 한다)가 충족되지 않은" 유형이라, 앞으로 비슷한 다단계 기능(여러 서비스에 걸친 공통 인프라)을 작업할 때는 "개별 항목 승인"과 "묶음 전체 목적 달성" 여부를 분리해서 리뷰하는 것이 유효했다.
