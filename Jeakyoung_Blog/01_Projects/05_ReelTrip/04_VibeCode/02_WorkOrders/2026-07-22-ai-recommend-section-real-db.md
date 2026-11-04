---
title: AI 추천 섹션 실 DB 연동
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
| **요구사항 참조** | 실DB 전환 작업 #3 — AiRecommendSection (DUMMY_PLACES) |
| **대상 앱** | Web |
| **대상 페이지/화면** | `/dashboard` (DashboardScreen > AiRecommendSection) |
| **작업 유형** | 실DB 전환 |
| **예상 영향 범위** | dashboard/DashboardScreen.tsx |

---

## 요구사항 분석 요약

- `AiRecommendSection` 컴포넌트가 `DUMMY_PLACES` 상수를 직접 참조 중
- `place/api.ts`에 `listPlaces(spaceId, token)` 함수가 이미 존재하므로 연동만 하면 됨
- `PlaceResponse`에는 `name`, `region`, `tags`, `thumbnailUrl`, `category` 등 필요한 필드가 모두 있음

**[?] 섹션 제목 확인 필요:**
현재 섹션 제목이 "AI 추천 장소"이지만, `listPlaces()`로 가져오는 데이터는 팀원들이 URL 파서로 **직접 저장한 장소**입니다.
실제 AI 추천 기능은 `AiScreen.tsx`의 `DUMMY_AI_RECS`가 별도로 존재합니다.
→ 제목을 **"저장된 장소"** 로 변경하는 것이 맞는지 확인이 필요합니다.

**구조 차이:**

| 항목 | DUMMY_PLACES | PlaceResponse (실 데이터) |
|------|--------------|--------------------------|
| 이름 | `name` | `name` |
| 지역 | `region` (string) | `region` (string \| null) |
| 태그 | `tags: string[]` (예: `"#바다"`) | `tags: string[]` (예: `"바다"`) |
| 썸네일 | 없음 (🏖️ 고정 이모지) | `thumbnailUrl: string \| null` |
| 카테고리 | 없음 | `category: string \| null` |

---

## 작업 계획

### 1단계: DashboardInner에 places 상태 및 fetch 추가
- [ ] `places` state 추가: `useState<PlaceResponse[]>([])`
- [ ] `listPlaces` import 추가
- [ ] `selectedSpaceId` 변경 시 `listPlaces(spaceId, token)` 호출하는 useEffect 추가 (#1 events fetch와 동일한 패턴)

### 2단계: AiRecommendSection 컴포넌트 수정
- [ ] props 추가: `places: PlaceResponse[]` 수신
- [ ] `DUMMY_PLACES` 상수 제거
- [ ] 카드 렌더링 수정:
  - 썸네일: `thumbnailUrl` 있으면 `<img>` 표시, 없으면 기존 gradient + 이모지 fallback 유지
  - 지역: `region ?? country ?? "-"` 순으로 fallback
  - 태그: `PlaceResponse.tags`를 `#` 붙여서 표시
  - 최대 3개 카드만 표시 (대시보드 요약 화면)
- [ ] places 없을 때 빈 상태 메시지: `"저장된 장소가 없습니다"`
- [ ] 하단 페이지네이션 dot 제거 (하드코딩 5개 → 실 데이터 기반 의미 없음)

### 3단계: DashboardInner에서 props 전달
- [ ] `<AiRecommendSection />` 호출부에 `places={places.slice(0, 3)}` 전달

---

## 변경 대상 파일

| 파일 경로 | 변경 유형 | 변경 내용 요약 |
|-----------|-----------|----------------|
| `apps/web/src/domains/dashboard/components/DashboardScreen.tsx` | 수정 | `DUMMY_PLACES` 제거, `places` 상태 추가, `listPlaces` 연동, `AiRecommendSection` props 추가 |

---

## 사이드 이펙트 검토

- `AiRecommendSection`은 `DashboardScreen` 내부 컴포넌트 — 외부 사용처 없음
- `listPlaces`는 `DashboardScreen` 상단에서 이미 `addPlace`로 import 중 — 동일 파일에서 추가 import만 하면 됨
- places fetch는 events fetch와 동일하게 `selectedSpaceId` 변경 시 재요청

---

## 확인 필요 사항

- [ ] 섹션 제목 "AI 추천 장소" → "저장된 장소"로 변경할지 여부

---

## 컨펌

- [ ] 위 계획대로 진행 승인
- [ ] 수정 후 재검토 필요
